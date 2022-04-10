"""
蓝图：用户认证
"""
import logging

from flask import jsonify, request
from flask.blueprints import Blueprint

from backend.blueprint import get_system_guest_role
from backend.data.basic_carrier import BasicCarrier
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.master_user_em import MasterUserEm, MasterUserRegisterEm
from backend.service.master_user_service import try_login_user, try_register_user
from backend.utility.error_helper import BusinessError
from backend.utility.route_premission_helper import RoutePermissionHelper

auth_blueprint = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth",
)
route_permission = RoutePermissionHelper(auth_blueprint, group="登录")


@auth_blueprint.route("/login", methods=["POST"])
@route_permission.set(login_required=False, allow_all=True, name="用户登录")
def route_login():
    carrier = BasicCarrier()
    try:
        data = request.get_json()
        with SqlAlchemyUOW(
            handler=get_system_guest_role(),
            action="try-login",
            action_params={
                **data,
                # "headers": request.headers,
            },
        ) as uow:
            carrier.result = try_login_user(
                user_em=MasterUserEm(**data),
                transaction=uow.transaction,
            )
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict(to_camel=True))


# @auth_blueprint.route("/logout", methods=["GET"])
# @route_permission.set(comment="登录-用户登出")
# def route_logout():
#     carrier = BasicCarrier()
#     if current_user.is_authenticated:
#         logout_user()
#         carrier.data = {"status": "You are not logged in now."}
#     else:
#         carrier.data = {"status": "You have not logged in yet."}
#     return jsonify(carrier.dict())


@auth_blueprint.route("/register", methods=["POST"])
@route_permission.set(login_required=False, allow_all=True, name="用户注册")
def route_register():
    carrier = BasicCarrier()
    try:
        data = request.get_json()
        with SqlAlchemyUOW(
            handler=get_system_guest_role(),
            action="register",
            action_params={"username": data["username"]},
        ) as uow:
            user_id = try_register_user(
                user_em=MasterUserRegisterEm(**data), transaction=uow.transaction
            )
            if user_id is not None:
                carrier.result = {"status": "success", "user_id": user_id}
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())
