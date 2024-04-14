from flask import Flask
from src.application_container import AppContainer, Core
from src.controller import blueprint as endpoints
from src.controller.routes import health_check as health_check_module
from src.infrastructure.database import get_database_url


def create_app() -> Flask:
    database_url = get_database_url()
    Core.config.override({"database_url": database_url})

    container = AppContainer()
    container.wire(modules=[health_check_module])

    app = Flask(__name__)
    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["ERROR_INCLUDE_MESSAGE"] = False
    app.register_blueprint(blueprint=endpoints)

    return app
