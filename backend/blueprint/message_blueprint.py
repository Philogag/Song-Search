import logging

from flask import Blueprint, request

from backend.blueprint import basic_carrier_result, get_current_user_handler, get_current_user_id
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.service.message_service import get_unchecked_message, set_message_checked
from backend.utility.route_premission_helper import RoutePermissionHelper

message_blueprint = Blueprint(name="message", import_name=__name__, url_prefix="/message")
route_permission = RoutePermissionHelper(message_blueprint, group="消息")
logger = logging.getLogger(__name__)


@message_blueprint.route("/check-new", methods=["POST"])
@route_permission.set(name="查询新消息")
@basic_carrier_result()
def route_get_songs_source_page():
    query = request.get_json(silent=True)
    return get_unchecked_message(
        user_id=get_current_user_id(),
        after=query['after'] if 'after' in query.keys() else None
    )


@message_blueprint.route("/set-message-checked/<string:message_id>", methods=["GET"])
@route_permission.set(name="标记消息已查看")
@basic_carrier_result()
def route_search(message_id: str):
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="check-message",
        action_params={
            "message_id": message_id,
        },
    ) as uow:
        return set_message_checked(message_id, transaction=uow.transaction)
