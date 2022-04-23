from sqlalchemy import Column, String, Integer

from backend.model.basic_entity import BasicHistoryEntity


class SongsSourceHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_songs_source_history"

    title = Column(String(255), comment="标题")
    author = Column(String(40), comment="作者")
    dynasty = Column(String(20), comment="朝代")
    content = Column(String(2000), comment="正文")
    tags = Column(String(2000), comment="标签")
    int_id = Column(Integer, comment="数字id", index=True)
