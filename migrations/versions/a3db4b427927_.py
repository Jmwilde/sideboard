"""Add favorites and purchased tables. Add email to customers.

Revision ID: a3db4b427927
Revises: 8b0cc81f2f38
Create Date: 2022-03-24 22:59:19.352277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3db4b427927'
down_revision = '8b0cc81f2f38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('customer_id', 'item_id')
    )
    op.create_table('purchased',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('customer_id', 'item_id')
    )
    op.add_column('customers', sa.Column('email', sa.String(length=100), nullable=False))
    op.alter_column('items', 'merchant_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'merchant_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('customers', 'email')
    op.drop_table('purchased')
    op.drop_table('favorites')
    # ### end Alembic commands ###
