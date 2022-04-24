from typing import Optional

from pydantic import Field

from backend.data.system_enum import EnumMessageStatus
from backend.model.basic_model import BasicEditModel


class MessageEm(BasicEditModel):
    receiver: str
    title: str
    content: Optional[str]
    status: str = Field(default=EnumMessageStatus.running.name)
    checked: bool = Field(default=False)
