from datetime import datetime
from typing import Optional

from backend.model.basic_model import BasicEditModel


class SearchLogEm(BasicEditModel):
    search_text: str
    status: str
    create_at: Optional[datetime] = datetime.utcnow()
    user_meta: str
