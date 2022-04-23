import os
from typing import Optional, Union

import toml
from pydantic import BaseModel

from backend.utility.error_helper import BusinessError


class DevConfig(BaseModel):
    debug = True


class LoggerConfig(BaseModel):
    config_file: str


class ConnectionConfig(BaseModel):
    type: Optional[str]
    host: str
    port: Optional[Union[int, str]]
    db: Optional[Union[int, str]]
    username: Optional[str]
    password: Optional[str]

    def get_uri(self):
        return f"{self.type}://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"


class JWTConfig(BaseModel):
    secret_key: str = "jwt-secret-key_"
    token_location: str = ""
    access_token_expires: int
    refresh_token_expires: int


class FlaskConfig(BaseModel):
    app_name: str

    secret_key: str
    timezone: str = "Asia/Shanghai"

    db: ConnectionConfig
    redis: ConnectionConfig
    rabbit_mq: ConnectionConfig
    milvus: ConnectionConfig
    jwt: JWTConfig
    logger: LoggerConfig


def load_config_from_toml(filepath) -> FlaskConfig:
    if os.path.isfile(filepath):
        config_dict = toml.load(filepath)
        return FlaskConfig(**config_dict)
    else:
        raise BusinessError("配置文件不存在")
