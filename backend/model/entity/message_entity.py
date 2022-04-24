from sqlalchemy import Column, String, Boolean

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.message_history import MessageHistoryEntity


class MessageEntity(BasicVersionControlledEntity):
    __tablename__ = "st_message"
    __history_entity__ = MessageHistoryEntity

    receiver = Column(String(40), comment="接收人", nullable=False)
    title = Column(String(40), comment="标题", nullable=False)
    content = Column(String(1000), comment="正文", nullable=True)
    status = Column(String(20), comment="状态", nullable=False)
    checked = Column(Boolean, comment="已查看", nullable=False, default=False)
