from database import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import Store
from schemas import StoreSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores/<string:id>")
class StoreRetrieveAndDelete(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, id):
        store = Store.query.get_or_404(id)
        return store

    def delete(self, id):
        store = Store.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}, 204


@blp.route("/stores")
class StoreListAndCreate(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return Store.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = Store(**store_data)

        try:
            db.session.add(store)
            db.session.commit()

        except IntegrityError:
            abort(400, message="A Store with that name already exists.")

        except SQLAlchemyError:
            abort(
                500,
                message="An error ocurred wwhile inserting the item into database.",  # noqa E501
            )

        return store, 201
