
from typing import Optional
from pydantic import BaseModel


class SearchLogDetailVm(BaseModel):
    """搜索记录结果-用于库查询"""
    model_name: str
    result_title: str
    result_author: str
    result_dynasty: str
    result_confidence: float
    user_feedback: Optional[float]


class SearchLogGuestDetailVm(BaseModel):
    """搜索记录结果-用于用户结果展示"""
    id: str
    title: str
    author: str
    dynasty: str
    content: str
    result_confidence: float
    user_feedback: Optional[float]
