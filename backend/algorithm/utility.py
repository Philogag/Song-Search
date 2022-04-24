import uuid
from typing import List

import pymilvus
from datetime import datetime

from backend.data.system_enum import EnumRobotCode, EnumMessageStatus
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.message_em import MessageEm
from backend.model.edit.model_meta_em import ModelMetaEm
from backend.repository.message_repository import MessageRepository
from backend.repository.model_meta_repository import ModelMetaRepository
from backend.repository.robot_repository import RobotRepository
from backend.repository.songs_source_repository import SongsSourceRepository


def get_system_message_queue_robot():
    return RobotRepository.get_by_params({"code": EnumRobotCode.message_queue_robot.name})


def uint64_to_int64(num):
    flag = -1 if ((num >> 63) & 1) == 1 else 1
    return flag * num - (1 << 63)


def uuid_to_double_int64(uuid_str: str):
    u = uuid.UUID(uuid_str)
    uint = int(u)
    i64 = (1 << 64)
    u1, u2 = (uint >> 64), uint % i64
    if not(u1 <= i64 and u2 <= i64):
        print(uuid_str)
    return u1, u2


def double_int64_to_uuid(int1, int2):
    return str(uuid.UUID(int=((int1 << 64) + int2)))


def get_or_create_model_meta(model_id: int, model_name: str = None):
    with SqlAlchemyUOW(
        handler=get_system_message_queue_robot(),
        action="create-model-meta",
        action_params={"model_id": model_id, "model_name": model_name},
    ) as uow:
        return ModelMetaRepository.get_or_create_model_meta(
            data=ModelMetaEm(
                model_id=model_id,
                model_name=model_name,
            ),
            transaction=uow.transaction
        )


def get_train_data(model_em: ModelMetaEm, force_all=False):
    if not force_all and model_em.last_train_at is not None:
        data = SongsSourceRepository.fetch_create_after_time(model_em.last_train_at)
    else:
        data = SongsSourceRepository.fetch_create_after_time()
    model_em.last_train_at = datetime.now()
    with SqlAlchemyUOW(
        handler=get_system_message_queue_robot(),
        action="train-model",
        action_params={"id": model_em.id},
    ) as uow:
        ModelMetaRepository.update_entity(model_em, transaction=uow.transaction, col_list=["last_train_at"])
    return data


def finish_message(message_id: str, title: str = None, content: str = None, success: bool = True):
    message_em: MessageEm = MessageRepository.fetch_by_id(message_id)

    message_em.checked = False
    message_em.status = EnumMessageStatus.success.name if success else EnumMessageStatus.failed.name
    if title:
        message_em.title = title
    if content:
        message_em.content = content

    with SqlAlchemyUOW(
        handler=get_system_message_queue_robot(),
        action="update-message",
        action_params=message_em.dict(),
    ) as uow:
        MessageRepository.update_entity(message_em, transaction=uow.transaction)
