"""empty message

Revision ID: 5c78a3f615eb
Revises: 9d2863e991a0
Create Date: 2023-03-07 16:41:48.287505

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c78a3f615eb'
down_revision = '9d2863e991a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_items', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', mysql.DECIMAL(precision=10, scale=2), nullable=False))

    # ### end Alembic commands ###
