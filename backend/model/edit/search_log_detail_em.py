from backend.model.basic_model import BasicEditModel


class SearchLogDetailEm(BasicEditModel):
    search_log_id: str
    model_id: str

    result_song_id: str
    result_confidence: float
    user_feedback: float
