from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ModelMetaEm(BaseModel):
    id: Optional[str]
    model_id: int
    model_name: Optional[str]
    last_heart_beat: Optional[datetime]
    last_train_at: Optional[datetime]

    def to_orm_dict(self, flat=True):
        return self.dict()
