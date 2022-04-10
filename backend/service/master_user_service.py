from datetime import datetime
from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token

from backend.blueprint import generate_jwt_payload
from backend.data.pagination_carrier import PaginationCarrier, PaginationParams
from backend.data.transaction import Transaction
from backend.model.edit.master_user_em import MasterUserEm, MasterUserManageEm, MasterUserRegisterEm
from backend.model.view.master_user_info_vm import MasterUserInfoVm
from backend.model.view.master_user_list_vm import MasterUserListVm
from backend.repository.master_user_repository import MasterUserRepository
from backend.repository.user_role_map_repository import UserRoleMapRepository
from backend.service.role_service import set_user_role_list
from backend.utility.error_helper import BusinessError
from backend.utility.string_helper import is_fake_uuid


def get_user_em_by_id(user_id) -> Optional[MasterUserEm]:
    return MasterUserRepository.get_by_id(user_id=user_id)


def try_login_user(*, user_em: MasterUserEm, transaction: Transaction):
    exist_user = MasterUserRepository.get_by_params(
        params={"username": user_em.username}
    )
    if not exist_user:
        raise BusinessError("Username not exist.")

    if not exist_user.check_password(user_em.password):
        raise BusinessError("Password wrong.")

    exist_user.last_login_at = datetime.now()
    MasterUserRepository.update_user(
        data=exist_user, transaction=transaction, col_list={"last_login_at"}
    )

    token_payload = generate_jwt_payload(
        user_id=exist_user.id,
    )

    access_token = create_access_token(identity=token_payload)
    refresh_token = create_refresh_token(identity=token_payload)

    current_role = UserRoleMapRepository.get_user_current_role_by_user_id(exist_user.id)

    return {
        "user_id": exist_user.id,
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        "role": current_role,
    }


def try_register_user(
    *, user_em: MasterUserRegisterEm, transaction: Transaction
) -> str:
    exist_user = MasterUserRepository.get_by_params(
        params={"username": user_em.username}
    )
    if exist_user:
        raise BusinessError("Username exist.")

    if not user_em.check_password2():
        raise BusinessError("Password verified failed.")

    user_em.encrypt_password()
    user_id = MasterUserRepository.insert_user(user_em=user_em, transaction=transaction)

    if user_id:
        return user_id
    else:
        raise BusinessError("Register failed.")


def get_user_info(user_id: str) -> Optional[MasterUserInfoVm]:

    user_info = MasterUserRepository.get_user_info(user_id=user_id)

    user_info.current_role = UserRoleMapRepository.get_user_current_role_by_user_id(
        user_id=user_id
    )
    user_info.roles = UserRoleMapRepository.fetch_roles_by_user_id(user_id)
    return user_info


def get_user_list_for_management(
    params: PaginationParams,
) -> PaginationCarrier[MasterUserListVm]:
    return MasterUserRepository.get_organization_list_page(params=params)


def create_or_update_master_user(data: MasterUserManageEm, transaction: Transaction):
    if is_fake_uuid(data.id):
        data.check_new_password()
        MasterUserRepository.create_entity(data, transaction)
    else:
        if data.check_new_password():
            col_list = None
        else:
            col_list = ["username", "is_active"]
        MasterUserRepository.update_entity(data, transaction, col_list)

    if not data.organization_id:
        raise BusinessError("用户所属组织不得为空")

    set_user_role_list(
        user_id=data.id, role_id_list=data.role_id_list, transaction=transaction
    )


def delete_master_user(user_id: str, transaction: Transaction):
    MasterUserRepository.delete_entity_by_id(entity_id=user_id, transaction=transaction)
