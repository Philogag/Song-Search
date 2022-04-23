import json
from typing import List

from backend.data.pagination_carrier import PaginationParams, PaginationCarrier
from backend.data.transaction import Transaction
from backend.model.edit.songs_source_em import SongsSourceEm
from backend.model.view.songs_source_vm import SongsSourceVm
from backend.repository.songs_source_repository import SongsSourceRepository
from backend.utility.error_helper import BusinessError


def get_songs_source_page(params: PaginationParams) -> PaginationCarrier[SongsSourceVm]:
    return SongsSourceRepository.fetch_page(params)


def save_import_songs(data_list: List[SongsSourceEm], transaction: Transaction):
    for d in data_list:
        SongsSourceRepository.create_entity(
            data=d,
            transaction=transaction,
        )


def import_file(file, transaction: Transaction):
    file_handler = {
        'json': scan_import_json_file,
    }
    file_ext = file.filename.split('.')[-1]
    assert file_ext in file_handler.keys(), BusinessError("不支持的文件格式")
    data = file_handler[file_ext](file)
    save_import_songs(data, transaction)


def scan_import_json_file(file) -> List[SongsSourceEm]:
    data = json.load(file)
    return [SongsSourceEm(**d) for d in data]
