from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.model.view.songs_source_vm import SongsSourceVm
from backend.repository.songs_source_repository import SongsSourceRepository


def get_songs_source_page(params: PaginationParams) -> PaginationCarrier[SongsSourceVm]:
    return SongsSourceRepository.fetch_page(params)
