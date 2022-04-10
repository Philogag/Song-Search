from pydantic import BaseModel


class CurrentUserInfo(BaseModel):
    id: str
    organization_id: str
    current_role_code: str
