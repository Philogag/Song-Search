from datetime import datetime

from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.model.edit.songs_source_em import SongsSourceEm
from backend.model.entity.songs_source_entity import SongsSourceEntity
from backend.model.view.songs_source_vm import SongsSourceVm
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder


class SongsSourceRepository(BasicRepository):
    __entity_cls__ = SongsSourceEntity
    __model_cls__ = SongsSourceEm

    @classmethod
    def fetch_page(cls, params: PaginationParams) -> PaginationCarrier[SongsSourceVm]:
        sql = """
        select *, sss.handled_at as created_at from st_songs_source sss
        """

        pagination_query = PaginationQueryBuilder(
            result_type=SongsSourceVm,
            sql=sql,
            search_columns=['title', 'author'],
            filter_columns=['dynasty'],
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
    def fetch_create_after_time(cls, filter_time: datetime = None):
        sql = "select * from st_songs_source sss "
        if filter_time:
            sql += " where sss.handled_at >= :filter_time"
        return cls._fetch_all(
            model_cls=SongsSourceEm,
            sql=sql,
            params={"filter_time": filter_time},
        )
