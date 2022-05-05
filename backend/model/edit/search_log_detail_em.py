
from typing import Optional, Union

from backend.model.basic_model import BasicEditModel


class SearchLogDetailEm(BasicEditModel):
    search_log_id: str
    model_id: str

    result_song_id: Optional[Union[str, int]]
    result_confidence: Optional[float]
    user_feedback: Optional[float]
