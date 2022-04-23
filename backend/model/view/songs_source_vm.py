from datetime import datetime

from backend.model.edit.songs_source_em import SongsSourceEm


class SongsSourceVm(SongsSourceEm):
    created_at: datetime
