import json
import logging
from collections import Callable
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from backend.data.basic_carrier import BasicCarrier
from backend.data.system_enum import EnumRobotCode, EnumRoleCode
from backend.model.edit.master_user_em import MasterUserEm
from backend.model.view.current_user_vm import CurrentUserInfo
from backend.repository.robot_repository import RobotRepository
from backend.repository.role_repository import RoleRepository
from backend.service.role_service import get_user_current_role_code
from backend.utility.error_helper import BusinessError


def basic_carrier_result() -> Callable:
    """
    1. Set the result into `BasicCarrier.result`
    2. Call the `jsonify(carrier.to_dict())` to serialize the Response
    3. Catch all BusinessError Exception
    """

    def __actual_result_build(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            carrier = BasicCarrier()
            try:
                carrier.result = func(
                    *args, **kwargs
                )  # Call the actual function to get the result data.
            except BusinessError as err:
                logging.exception(err)
                carrier.push_exception(err)
            return jsonify(carrier.to_dict())

        return wrapper

    return __actual_result_build


def get_system_guest_role():
    return RoleRepository.get_role_by_code(code=EnumRoleCode.guest.name)


def get_system_init_robot():
    return RobotRepository.get_by_params({"code": EnumRobotCode.init_robot.name})


def generate_jwt_payload(**kargs):
    return json.dumps(dict(**kargs))


def get_jwt_payload():
    try:
        return json.loads(get_jwt_identity())
    except Exception:
        return None


def get_current_user_id():
    payload = get_jwt_payload()
    if payload is not None:
        return payload["user_id"]
    else:
        raise BusinessError('user not login.')


def get_current_user_handler():
    return MasterUserEm(
        id=get_current_user_id(),
        username="",
        password="",
    )


def get_current_user_info():
    user_id = get_current_user_id()
    return CurrentUserInfo(
        id=user_id,
        current_role_code=get_user_current_role_code(user_id),
    )