from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.data.transaction import Transaction
from backend.factory import message_queue
from backend.model.edit.message_em import MessageEm
from backend.model.edit.model_meta_em import ModelMetaEm
from backend.repository.message_repository import MessageRepository
from backend.repository.model_meta_repository import ModelMetaRepository
from backend.utility.error_helper import BusinessError


def get_model_meta_page(params: PaginationParams) -> PaginationCarrier[ModelMetaEm]:
    return ModelMetaRepository.fetch_page(params)


def run_train(model_id: str, force_all=False, transaction: Transaction = None):
    model_meta: ModelMetaEm = ModelMetaRepository.fetch_by_id(model_id)
    assert model_meta is not None, BusinessError('模型不存在')

    message_id = MessageRepository.create_entity(
        MessageEm(
            receiver=transaction.handler_id,
            title="训练模型" if not force_all else "重置模型",
        ),
        transaction=transaction,
    )

    if force_all:
        message_queue.push_task(channel=model_meta.model_name, method='reset', data={"message_id": message_id})
    else:
        message_queue.push_task(channel=model_meta.model_name, method='train', data={"message_id": message_id})
    return 'Running.'
