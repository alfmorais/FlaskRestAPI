"""empty message

Revision ID: 5fd914434ab7
Revises: b5249ade9ce3
Create Date: 2023-05-29 12:20:20.909862

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5fd914434ab7"
down_revision = "b5249ade9ce3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "username",
            existing_type=sa.VARCHAR(length=80),
            type_=sa.String(length=256),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "password",
            existing_type=sa.VARCHAR(length=80),
            type_=sa.String(length=256),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "password",
            existing_type=sa.String(length=256),
            type_=sa.VARCHAR(length=80),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "username",
            existing_type=sa.String(length=256),
            type_=sa.VARCHAR(length=80),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
