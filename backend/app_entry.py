"""
入口
"""
import os

from backend.factory import create_flask_app
from backend.utility.config_helper import load_config_from_toml

app_config_toml = os.getenv("FLASK_CONFIG_TOML")
app_config_toml = (
    app_config_toml if app_config_toml else "./backend/app.development.toml"
)

flask_app = create_flask_app(load_config_from_toml(app_config_toml))

if __name__ == "__main__":
    flask_app.run(debug=True)
