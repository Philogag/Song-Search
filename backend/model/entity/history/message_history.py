from sqlalchemy import Column, String, Boolean

from backend.model.basic_entity import BasicHistoryEntity


class MessageHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_message_history"

    receiver = Column(String(40), comment="接收人", nullable=False)
    title = Column(String(40), comment="标题", nullable=False)
    content = Column(String(1000), comment="正文", nullable=True)
    status = Column(String(20), comment="状态", nullable=False)
    checked = Column(Boolean, comment="已查看", nullable=False, default=False)

