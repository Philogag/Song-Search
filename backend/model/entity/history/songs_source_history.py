from sqlalchemy import Column, String

from backend.model.basic_entity import BasicHistoryEntity


class SongsSourceHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_songs_source_history"

    title = Column(String(255), comment="标题")
    author = Column(String(40), comment="作者")
    dynasty = Column(String(20), comment="朝代")
    content = Column(String(2000), comment="正文")
