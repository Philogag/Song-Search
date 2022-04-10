from typing import Optional

from backend.model.basic_model import BasicEditModel


class CompetitionResultEm(BasicEditModel):
    people_id: str

    competition_id: str

    competition_group: Optional[int]
    competition_group_order: Optional[int]
    competition_step: Optional[str]

    result: Optional[float]
    result_invalid: Optional[bool] = False
    result_invalid_comment: Optional[str]

    rating_score: Optional[float]
