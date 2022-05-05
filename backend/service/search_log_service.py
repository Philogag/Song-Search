
from typing import List

from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.data.system_enum import EnumSearchLogStatus
from backend.data.transaction import Transaction
from backend.factory import message_queue
from backend.model.edit.search_log_em import SearchLogEm
from backend.model.view.search_log_vm import SearchLogVm
from backend.model.view.search_log_detail_vm import SearchLogGuestDetailVm
from backend.repository.search_log_repository import SearchLogRepository
from backend.repository.search_log_detail_repository import SearchLogDetailRepository
from backend.utility.error_helper import BusinessError


def get_search_log_page(params: PaginationParams) -> PaginationCarrier[SearchLogVm]:
    return SearchLogRepository.fetch_page(params)


def do_search(search_text: str, model_name: str = 'jiayan+word2vec+cos', transaction: Transaction = None):
    search_id = SearchLogRepository.create_entity(
        data=SearchLogEm(
            search_text=search_text,
            status=EnumSearchLogStatus.create.name,
        ),
        transaction=transaction,
    )
    message_queue.push_task(
        channel=model_name,
        method='search',
        data={
            "search_id": search_id,
            "search_text": search_text
        }
    )
    return {"search_log_id": search_id}


def get_search_result(search_log_id: str) -> List[SearchLogGuestDetailVm]:
    return SearchLogRepository.fetch_result(search_log_id)


def set_search_log_detail_score(search_log_detail_id: str, score: float, transaction: Transaction):
    detail = SearchLogDetailRepository.fetch_by_id(search_log_detail_id)
    assert detail is not None, BusinessError('结果不存在')
    detail.user_feedback = score
    SearchLogDetailRepository.update_entity(detail, transaction, col_list=['user_feedback'])
