from datetime import datetime

from backend.model.edit.message_em import MessageEm


class MessageVm(MessageEm):
    handled_at: datetime
