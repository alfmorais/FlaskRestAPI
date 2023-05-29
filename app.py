import os

from blocklist import BLOCKLIST
from database import db
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from models import Item, ItemTags, Store, Tag, User  # noqa F401
from resources.items import blp as ItemsBlueprint
from resources.stores import blp as StoresBlueprint
from resources.tags import blp as TagsBlueprint
from resources.users import blp as UsersBlueprint


def create_app(db_url=None):
    # Main instance of Flask APP
    app = Flask(__name__)
    load_dotenv()

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

    # Database / Alembic / Migrate Configuration
    migrate = Migrate(app, db)

    # Blueprints
    api = Api(app)

    # JWT Configuration
    app.config["JWT_SECRETY_KEY"] = "84466196-47cb-4bdb-8b2a-f4a157cc34fe"

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_blocklist_loader(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    # JWT Standard Responses
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "token_revoked",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token is not fresh.",
                    "error": "fresh_token_required.",
                }  # noqa E501
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token has expired.",
                    "error": "token_expired",
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed.",
                    "error": "invalid_token",
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # Blueprints configuration
    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(StoresBlueprint)
    api.register_blueprint(TagsBlueprint)
    api.register_blueprint(UsersBlueprint)

    return app
