from pydantic import BaseModel


class SearchLogDetailVm(BaseModel):
    model_name: str
    result_content: str
    result_confidence: float
    user_feedback: float
