from backend.model.basic_model import BasicEditModel


class SongsSourceEm(BasicEditModel):
    title: str
    author: str
    dynasty: str
    content: str
    int_id: int
