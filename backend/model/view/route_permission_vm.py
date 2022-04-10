from typing import Any, List, Optional, Union

from pydantic import BaseModel


class RoutePermissionVm(BaseModel):
    route_path: str
    need_login: bool
    allow_all: bool

    menu_list: Any
    role_list: Any
