from datetime import datetime

from sqlalchemy import Column, String, DateTime

from backend.model.basic_entity import BasicHistoryEntity


class SearchLogHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_search_log_history"

    search_text = Column(String(255), comment="用户输入")
    status = Column(String(20), comment="状态")
    create_at = Column(DateTime(timezone=True), comment="查询时间", default=datetime.utcnow)
    user_meta = Column(String(1000), comment="用户信息", default="{}")
