from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.factory import message_queue
from backend.model.edit.model_meta_em import ModelMetaEm
from backend.repository.model_meta_repository import ModelMetaRepository


def get_model_meta_page(params: PaginationParams) -> PaginationCarrier[ModelMetaEm]:
    return ModelMetaRepository.fetch_page(params)


def run_train():
    message_queue.push_task(channel="jiayan+word2vec+cos", method='train', data={})
    return 'Running.'
