import logging

from flask import Blueprint, request

from backend.blueprint import basic_carrier_result
from backend.data.pagination_carrier import PaginationParams
from backend.service.search_log_service import do_search
from backend.service.songs_source_service import get_songs_source_page
from backend.utility.route_premission_helper import RoutePermissionHelper

search_blueprint = Blueprint(name="search", import_name=__name__, url_prefix="/search")
route_permission = RoutePermissionHelper(search_blueprint, group="搜索")
logger = logging.getLogger(__name__)


@search_blueprint.route("/", methods=["GET"])
@route_permission.set(name="搜索")
@basic_carrier_result()
def route_search():
    search_text = request.args.get('search_text')
    model = request.args.get('model', default='*')
    return do_search(search_text=search_text, model=model)


@search_blueprint.route("/logs/get-page", methods=["POST"])
@route_permission.set(name="分页查询")
@basic_carrier_result()
def route_get_search_log_page():
    query = request.get_json(silent=True)
    return get_songs_source_page(params=PaginationParams(**query))



