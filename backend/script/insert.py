"""
注册系统角色
"""
import json
import os

from flask_script import Command

from backend.blueprint import get_system_init_robot
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.songs_source_em import SongsSourceEm
from backend.repository.songs_source_repository import SongsSourceRepository


def get_abs_path(path_str: str):
    folder, _ = os.path.split(os.path.abspath(__file__))
    return os.path.join(folder, path_str)


class Insert(Command):
    @classmethod
    def run(cls):
        with open(get_abs_path('tangshi.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)

        with SqlAlchemyUOW(
            handler=get_system_init_robot(),
            action="inert-songs",
            action_params={},
        ) as uow:
            for d in data:
                SongsSourceRepository.create_entity(
                    data=SongsSourceEm(**d),
                    transaction=uow.transaction,
                )
