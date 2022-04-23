from typing import Optional

from backend.model.basic_model import BasicEditModel


class SongsSourceEm(BasicEditModel):
    title: str
    author: str
    dynasty: str
    tags: Optional[str]
    content: str
    int_id: Optional[int]
