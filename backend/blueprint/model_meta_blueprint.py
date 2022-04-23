import logging

from flask import Blueprint, request

from backend.blueprint import basic_carrier_result
from backend.service.model_meta_service import run_train
from backend.utility.route_premission_helper import RoutePermissionHelper

model_meta_blueprint = Blueprint(name="model_meta", import_name=__name__, url_prefix="/model-meta")
route_permission = RoutePermissionHelper(model_meta_blueprint, group="模型元数据")
logger = logging.getLogger(__name__)


@model_meta_blueprint.route("/run-train/<string:object_id>", methods=["GET"])
@route_permission.set(name="触发训练")
@basic_carrier_result()
def route_search(object_id: str):
    force_all = request.args.get('force_all', default=False)
    return run_train()
