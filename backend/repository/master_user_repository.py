from typing import Iterable, Optional

from backend.data.pagination_carrier import PaginationCarrier, PaginationParams
from backend.data.transaction import Transaction
from backend.model.edit.master_user_em import MasterUserEm
from backend.model.entity.master_user_entity import MasterUserEntity
from backend.model.view.master_user_info_vm import MasterUserInfoVm
from backend.model.view.master_user_list_vm import MasterUserListVm
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder


class MasterUserRepository(BasicRepository):

    __entity_cls__ = MasterUserEntity
    __model_cls__ = MasterUserEm

    @staticmethod
    def get_by_id(*, user_id: str) -> Optional[MasterUserEm]:
        return MasterUserRepository._get_model_by_id(
            model_cls=MasterUserEm, entity_cls=MasterUserEntity, model_id=user_id
        )

    @classmethod
    def get_user_info(cls, user_id: str) -> Optional[MasterUserInfoVm]:
        sql = """
        select smu.*
        from st_master_user smu
        where smu.id = :user_id
        """
        return cls._fetch_first(
            model_cls=MasterUserInfoVm, sql=sql, params={"user_id": user_id}
        )

    @staticmethod
    def get_by_params(*, params) -> Optional[MasterUserEm]:
        return MasterUserRepository._get_model_by_params(
            model_cls=MasterUserEm, entity_cls=MasterUserEntity, params=params
        )

    @staticmethod
    def insert_user(*, user_em: MasterUserEm, transaction: Transaction) -> str:
        return MasterUserRepository._insert_entity(
            entity_cls=MasterUserEntity, data=user_em, transaction=transaction
        )

    @staticmethod
    def update_user(
        *, data: MasterUserEm, transaction: Transaction, col_list: Iterable[str] = None
    ) -> Optional[MasterUserEm]:
        return MasterUserRepository._update_entity(
            entity_cls=MasterUserEntity,
            data=data,
            transaction=transaction,
            col_list=col_list,
        )

    @classmethod
    def get_organization_list_page(
        cls, params: PaginationParams
    ) -> PaginationCarrier[MasterUserListVm]:
        sql = """
        select smu.*, 
        smo.id as organization_id, smo.name as organization_name, 
        role.role_list 
        from st_master_user smu
        left join  user_organization_map uom on uom.user_id=smu.id
        left join st_master_organization smo on smo.id=uom.organization_id
        left join (
            select urm.user_id, json_agg(json_build_object(
                'id', sr.id,
                'role_name', sr.role_name
            )) as role_list from user_role_map as urm
            left join st_role sr on sr.id = urm.role_id
            group by urm.user_id
        ) as role on role.user_id=smu.id
        order by smu.username asc
        """

        pagination_query = PaginationQueryBuilder(
            result_type=MasterUserListVm,
            sql=sql,
            search_columns=["username"],
            order_columns=params.order_columns
            if params.order_columns is not None
            else {},
            params={},
        )
        return pagination_query.get_query_result(
            page_size=params.page_size,
            page_index=params.page_index,
            search_text=params.search_text,
        )
