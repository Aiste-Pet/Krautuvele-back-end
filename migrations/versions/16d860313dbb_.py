"""empty message

Revision ID: 16d860313dbb
Revises: 956ef143f509
Create Date: 2023-03-07 10:09:02.525078

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '16d860313dbb'
down_revision = '956ef143f509'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], name=op.f('fk_cart_items_cart_id_cart')),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name=op.f('fk_cart_items_product_id_product')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cart_items'))
    )
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_constraint('fk_cart_product_id_product', type_='foreignkey')
        batch_op.drop_column('quantity')
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('quantity', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('fk_cart_product_id_product', 'product', ['product_id'], ['id'])

    op.drop_table('cart_items')
    # ### end Alembic commands ###
