from database import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )

    store = db.relationship("Store", back_populates="tags")
    items = db.relationship(
        "Item", back_populates="tags", secondary="items_tags"
    )  # noqa E501
