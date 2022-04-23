import logging

from flask import Blueprint, request

from backend.blueprint import basic_carrier_result, get_current_user_handler
from backend.data.pagination_carrier import PaginationParams
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.service.songs_source_service import get_songs_source_page, import_file
from backend.utility.route_premission_helper import RoutePermissionHelper

songs_source_blueprint = Blueprint(name="songs_source", import_name=__name__, url_prefix="/songs-source")
route_permission = RoutePermissionHelper(songs_source_blueprint, group="古诗词数据源")
logger = logging.getLogger(__name__)


@songs_source_blueprint.route("/get-page", methods=["POST"])
@route_permission.set(name="分页查询")
@basic_carrier_result()
def route_get_songs_source_page():
    query = request.get_json(silent=True)
    return get_songs_source_page(params=PaginationParams(**query))


@songs_source_blueprint.route("/import", methods=["POST"])
@route_permission.set(name="导入")
@basic_carrier_result()
def route_import_songs_source():
    uploaded_file = request.files['file']
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="import-songs",
        action_params={},
    ) as uow:
        import_file(
            file=uploaded_file,
            transaction=uow.transaction,
        )
