import os

from database import db
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from models import Item, ItemTags, Store, Tag, User  # noqa F401
from resources.items import blp as ItemsBlueprint
from resources.stores import blp as StoresBlueprint
from resources.tags import blp as TagsBlueprint


def create_app(db_url=None):
    # Main instance of Flask APP
    app = Flask(__name__)

    # Documentation and Exceptions
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Blueprints
    api = Api(app)

    # JWT Configuration
    app.config["JWT_SECRETY_KEY"] = "84466196-47cb-4bdb-8b2a-f4a157cc34fe"
    jwt = JWTManager(app)  # noqa F841

    # Blueprints configuration
    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(StoresBlueprint)
    api.register_blueprint(TagsBlueprint)

    return app
