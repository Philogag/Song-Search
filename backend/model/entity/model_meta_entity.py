"""
模型元数据数据集
"""

from sqlalchemy import Column, String, DateTime, Integer

from backend.model.basic_entity import BasicEntity


class ModelMetaEntity(BasicEntity):
    __tablename__ = "st_model_meta"

    model_name = Column(String(255), comment="模型名称")
    model_id = Column(Integer, comment="模型Id", unique=True, index=True)
    last_heart_beat = Column(DateTime(timezone=True), comment="心跳", nullable=True)
    last_train_at = Column(DateTime(timezone=True), comment="上次训练时间", nullable=True)
