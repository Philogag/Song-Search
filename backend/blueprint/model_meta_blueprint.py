import logging

from flask import Blueprint, request

from backend.blueprint import basic_carrier_result, get_current_user_handler
from backend.data.pagination_carrier import PaginationParams
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.service.model_meta_service import run_train, get_model_meta_page
from backend.utility.route_premission_helper import RoutePermissionHelper

model_meta_blueprint = Blueprint(name="model_meta", import_name=__name__, url_prefix="/model-meta")
route_permission = RoutePermissionHelper(model_meta_blueprint, group="模型元数据")
logger = logging.getLogger(__name__)


@model_meta_blueprint.route("/get-page", methods=["POST"])
@route_permission.set(name="分页查询")
@basic_carrier_result()
def route_get_songs_source_page():
    query = request.get_json(silent=True)
    return get_model_meta_page(params=PaginationParams(**query))


@model_meta_blueprint.route("/run-train/<string:model_id>", methods=["GET"])
@route_permission.set(name="触发训练")
@basic_carrier_result()
def route_search(model_id: str):
    force_all = request.args.get('force_all', default='false') == 'true'
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="train-model",
        action_params={
            "model_id": model_id,
            "force_all": force_all,
        },
    ) as uow:
        return run_train(model_id, force_all=force_all, transaction=uow.transaction)
