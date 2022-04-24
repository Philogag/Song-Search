from datetime import datetime
from typing import List

from backend.data.transaction import Transaction
from backend.model.view.message_vm import MessageVm
from backend.repository.message_repository import MessageRepository


def get_unchecked_message(user_id: str, after: datetime = None) -> List[MessageVm]:
    return MessageRepository.get_user_message(user_id=user_id, after=after)


def set_message_checked(message_id: str, transaction: Transaction):
    return MessageRepository.set_message_checked(message_id=message_id, transaction=transaction)