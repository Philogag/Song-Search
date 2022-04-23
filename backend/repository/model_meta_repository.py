from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.data.transaction import Transaction
from backend.model.edit.model_meta_em import ModelMetaEm
from backend.model.entity.model_meta_entity import ModelMetaEntity
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder


class ModelMetaRepository(BasicRepository):
    __entity_cls__ = ModelMetaEntity
    __model_cls__ = ModelMetaEm

    @classmethod
    def fetch_page(cls, params: PaginationParams) -> PaginationCarrier[ModelMetaEm]:
        sql = """select * from st_model_meta"""

        pagination_query = PaginationQueryBuilder(
            result_type=ModelMetaEm,
            sql=sql,
            search_columns=['model_id', 'model_name'],
            filter_columns=[],
            order_columns={},
            params={},
        )
        return pagination_query.get_query_result(
            page_size=params.page_size,
            page_index=params.page_index,
            search_text=params.search_text,
            filter_option=params.filter_columns,
        )

    @classmethod
    def get_or_create_model_meta(cls, data: ModelMetaEm, transaction: Transaction) -> ModelMetaEm:
        if cls.check_entity_exist(model_id=data.model_id):
            return cls.get_first_entity_by_params({"model_id": data.model_id})
        else:
            data.id = cls.create_entity(data, transaction)
            return data
