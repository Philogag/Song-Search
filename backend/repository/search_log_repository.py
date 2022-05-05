
from typing import List

from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.model.edit.search_log_em import SearchLogEm
from backend.model.entity.search_log_entity import SearchLogEntity
from backend.model.view.search_log_detail_vm import SearchLogGuestDetailVm
from backend.model.view.search_log_vm import SearchLogVm
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder


class SearchLogRepository(BasicRepository):
    """搜索记录库"""
    __entity_cls__ = SearchLogEntity
    __model_cls__ = SearchLogEm

    @classmethod
    def fetch_page(cls, params: PaginationParams) -> PaginationCarrier[SearchLogVm]:
        sql = """
        select ssl.* 
        , detail.details
        from st_search_log ssl
        left join (
            select ssld.search_log_id
            ,json_agg(json_build_object(
            'id', ssld.id
                ,'model_id', smm.id
                ,'model_name', smm.model_name
                ,'result_title', sss.title
                ,'result_author', sss.author
                ,'result_dynasty', sss.dynasty
                ,'result_confidence', ssld.result_confidence
                ,'user_feedback', ssld.user_feedback
            )) as details
            from st_search_log_detail ssld
            left join st_model_meta smm on smm.id = ssld.model_id
            left join st_songs_source sss on sss.int_id::varchar = ssld.result_song_id
            group by ssld.search_log_id
        ) detail on detail.search_log_id=ssl.id
        """

        pagination_query = PaginationQueryBuilder(
            result_type=SearchLogVm,
            sql=sql,
            search_columns=['search_text'],
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
    
    @classmethod
    def fetch_result(cls, search_log_id: str) -> List[SearchLogGuestDetailVm]:
        sql = """
        select ssld.id, ssld.result_confidence, ssld.user_feedback
        ,sss.title
        ,sss.author
        ,sss.dynasty
        ,sss.content
        from st_search_log_detail ssld
        left join st_songs_source sss on sss.int_id::varchar = ssld.result_song_id
        where ssld.search_log_id=:search_log_id
        """
        return cls._fetch_all(
            SearchLogGuestDetailVm,
            sql,
            params={
                "search_log_id": search_log_id
            }
        )
