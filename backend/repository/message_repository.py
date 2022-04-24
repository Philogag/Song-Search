from datetime import datetime
from typing import List

from backend.data.system_enum import EnumMessageStatus
from backend.data.transaction import Transaction
from backend.model.edit.message_em import MessageEm
from backend.model.entity.message_entity import MessageEntity
from backend.model.view.message_vm import MessageVm
from backend.repository.basic_repository import BasicRepository
from backend.utility.error_helper import BusinessError


class MessageRepository(BasicRepository):
    __entity_cls__ = MessageEntity
    __model_cls__ = MessageEm

    @classmethod
    def get_user_message(cls, user_id: str, after: datetime = None) -> List[MessageVm]:
        sql = """
        select sm.*
        from st_message sm
        where sm.receiver = :user_id
          and sm.status <> :status_running
          and not sm.checked
        """
        if after is not None:
            sql += " sm.handled_at >= :after"
        return cls._fetch_all(
            model_cls=MessageVm,
            sql=sql,
            params={
                "user_id": user_id,
                "after": after,
                "status_running": EnumMessageStatus.running.name,
            }
        )

    @classmethod
    def set_message_checked(cls, message_id: str, transaction: Transaction):
        message_em: MessageEm = cls.fetch_by_id(message_id)
        assert message_em is not None, BusinessError('消息不存在')
        assert message_em.status != EnumMessageStatus.running.name, BusinessError('事件进行中')
        assert not message_em.checked, BusinessError('消息已查看')

        message_em.checked = True
        cls.update_entity(message_em, transaction=transaction, col_list=['checked'])



