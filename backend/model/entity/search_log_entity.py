"""
搜索记录数据集
"""
from datetime import datetime

from sqlalchemy import Column, String, DateTime

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.search_log_history import SearchLogHistoryEntity


class SearchLogEntity(BasicVersionControlledEntity):
    __tablename__ = "st_search_log"
    __history_entity__ = SearchLogHistoryEntity

    search_text = Column(String(255), comment="用户输入")
    status = Column(String(20), comment="状态")
    create_at = Column(DateTime(timezone=True), comment="查询时间", default=datetime.utcnow)
    user_meta = Column(String(1000), comment="用户信息", default="{}")
