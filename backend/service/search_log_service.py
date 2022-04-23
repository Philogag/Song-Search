from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.factory import message_queue
from backend.model.view.search_log_vm import SearchLogVm
from backend.repository.search_log_repository import SearchLogRepository


def get_search_log_page(params: PaginationParams) -> PaginationCarrier[SearchLogVm]:
    return SearchLogRepository.fetch_page(params)


def do_search(search_text: str, model: str):
    message_queue.push_task(channel="jiayan+word2vec+cos", method='search', data={"search_text": search_text})
    return 'Running.'
