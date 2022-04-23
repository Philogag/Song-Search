from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.model.edit.search_log_em import SearchLogEm
from backend.model.entity.search_log_entity import SearchLogEntity
from backend.model.view.search_log_vm import SearchLogVm
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder


class SearchLogRepository(BasicRepository):
    __entity_cls__ = SearchLogEntity
    __model_cls__ = SearchLogEm

    @classmethod
    def fetch_page(cls, params: PaginationParams) -> PaginationCarrier[SearchLogVm]:
        sql = """
        """

        pagination_query = PaginationQueryBuilder(
            result_type=SearchLogVm,
            sql=sql,
            search_columns=['search_text',],
            filter_columns=['status'],
            order_columns={},
            params={},
        )
        return pagination_query.get_query_result(
            page_size=params.page_size,
            page_index=params.page_index,
            search_text=params.search_text,
            filter_option=params.filter_columns,
        )