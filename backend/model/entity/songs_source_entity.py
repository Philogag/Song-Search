"""
古诗词源数据集
"""
from sqlalchemy import Column, String, Integer

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.songs_source_history import SongsSourceHistoryEntity


class SongsSourceEntity(BasicVersionControlledEntity):
    __tablename__ = "st_songs_source"
    __history_entity__ = SongsSourceHistoryEntity

    title = Column(String(255), comment="标题")
    author = Column(String(40), comment="作者")
    dynasty = Column(String(20), comment="朝代")
    content = Column(String(2000), comment="正文")
    int_id = Column(Integer, comment="数字id", autoincrement=1, index=True)
