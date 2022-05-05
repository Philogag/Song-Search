from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, Integer

from backend.model.basic_entity import BasicHistoryEntity


class SearchLogDetailHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_search_log_detail_history"

    search_log_id = Column(String(40), comment="搜索记录", index=True)
    model_id = Column(String(40), comment="用户输入", index=True)

    result_song_id = Column(Integer, comment="结果id", index=True)
    result_confidence = Column(Float, comment="结果置信度（模型）")
    user_feedback = Column(Float, comment="用户反馈")
