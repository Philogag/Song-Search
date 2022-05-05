import logging

from flask import Blueprint, request

from backend.blueprint import basic_carrier_result, get_system_guest_role
from backend.data.pagination_carrier import PaginationParams
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.service.search_log_service import (
    do_search,
    get_search_result,
    set_search_log_detail_score,
    get_search_log_page,
)
from backend.utility.route_premission_helper import RoutePermissionHelper

search_blueprint = Blueprint(name="search", import_name=__name__, url_prefix="/search")
route_permission = RoutePermissionHelper(search_blueprint, group="搜索")
logger = logging.getLogger(__name__)


@search_blueprint.route("/", methods=["GET"])
@route_permission.set(name="搜索", allow_all=True)
@basic_carrier_result()
def route_search():
    search_text = request.args.get('search_text')
    model = request.args.get('model', default='*')
    with SqlAlchemyUOW(
        handler=get_system_guest_role(),
        action="switch-current-role",
        action_params={"search_text": search_text, },
    ) as uow:
        return do_search(search_text=search_text, transaction=uow.transaction)


@search_blueprint.route("/logs/get-page", methods=["POST"])
@route_permission.set(name="分页查询")
@basic_carrier_result()
def route_get_search_log_page():
    query = request.get_json(silent=True)
    return get_search_log_page(params=PaginationParams(**query))


@search_blueprint.route("/get-result/<string:id>", methods=["GET"])
@route_permission.set(name="获取结果", allow_all=True)
@basic_carrier_result()
def route_get_search_result(id: str):
    return get_search_result(id)


@search_blueprint.route("/set-user-feedback/<string:detail_id>", methods=["GET"])
@route_permission.set(name="用户反馈", allow_all=True)
@basic_carrier_result()
def route_set_user_feedback(detail_id: str):
    score = request.args.get('score', default=None)
    with SqlAlchemyUOW(
        handler=get_system_guest_role(),
        action="set-feedback",
        action_params={"detail_id": detail_id, "score": score},
    ) as uow:
        return set_search_log_detail_score(detail_id, score, uow.transaction)
