from database import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import Item, Store, Tag
from schemas import TagAndItemSchema, TagSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tags", "tags", description="Operations on tags.")


@blp.route("/stores/<string:id>/tags")
class TagsInStoreListAndCreate(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, id):
        store = Store.query.get_or_404(id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, id):
        if Tag.query.filter(
            Tag.store_id == id, Tag.name == tag_data["name"]  # noqa E501
        ).first():
            abort(
                400,
                message="A tag with that name already exists in that store.",  # noqa E501
            )

        tag = Tag(**tag_data, id=id)

        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError as error:
            abort(500, message=str(error))

        return tag


@blp.route("/tags/<string:id>")
class TagRetrieve(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
        tag = Tag.query.get_or_404(id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",  # noqa E501
        example={"message": "tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",  # noqa E501
    )
    def delete(self, id):
        tag = Tag.query.get_or_404(id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()

            return {"message": "Tag deleted."}

        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa E501
        )


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = Item.query.get_or_404(item_id)
        tag = Tag.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = Item.query.get_or_404(item_id)
        tag = Tag.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {
            "message": "Item removed from tag.",
            "item": item,
            "tag": tag,
        }
