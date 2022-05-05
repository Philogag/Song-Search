
from backend.model.edit.search_log_detail_em import SearchLogDetailEm
from backend.model.entity.search_log_detail_entity import SearchLogDetailEntity
from backend.repository.basic_repository import BasicRepository


class SearchLogDetailRepository(BasicRepository):
    __entity_cls__ = SearchLogDetailEntity
    __model_cls__ = SearchLogDetailEm