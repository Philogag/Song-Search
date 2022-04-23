import uuid
from typing import List

import pymilvus
from datetime import datetime

from backend.data.system_enum import EnumRobotCode
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.model_meta_em import ModelMetaEm
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


def get_train_data_by_last_trained_at(model_em: ModelMetaEm):
    # data = SongsSourceRepository.fetch_create_after_time(model_em.last_train_at)
    data = SongsSourceRepository.fetch_create_after_time()
    model_em.last_train_at = datetime.now()
    with SqlAlchemyUOW(
        handler=get_system_message_queue_robot(),
        action="train-model",
        action_params={"id": model_em.id},
    ) as uow:
        ModelMetaRepository.update_entity(model_em, transaction=uow.transaction, col_list=["last_train_at"])
    return data

