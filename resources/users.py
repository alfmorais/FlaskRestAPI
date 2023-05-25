from database import db
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint, abort
from models import User
from passlib.hash import pbkdf2_sha256
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on Users.")


@blp.route("/register")
class UserCreate(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if User.query.filter(User.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        hashed_password = pbkdf2_sha256.hash(user_data["password"])

        user = User(
            username=user_data["username"],
            password=hashed_password,
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/users/<int:id>")
class UserRetrieveAndDelete(MethodView):
    @blp.response(200, UserSchema)
    def get(self, id):
        user = User.query.get_or_404(id)
        return user

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted."}, 200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = User.query.filter(
            User.username == user_data["username"],
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)

            return {"access_token": access_token}, 201

        abort(401, message="Invalid credentials.")
