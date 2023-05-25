from database import db
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from models import Item
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/items/<int:id>")
class ItemsRetrieveDeleteAndPut(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, id):
        item = Item.query.get_or_404(id)
        return item

    def delete(self, id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}, 204

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, id):
        item = Item.query.get(id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = Item(id=id, **item_data)

        db.session.add(item)
        db.session.commit()

        raise item


@blp.route("/items")
class ItemsListAndCreate(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return Item.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, items_data):
        item = Item(**items_data)

        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(
                500,
                message="An error ocurred wwhile inserting the item into database.",  # noqa E501
            )

        return item, 201
