"""empty message

Revision ID: c71f6453f5dc
Revises: 78f92d28db07
Create Date: 2023-04-12 17:55:26.467378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c71f6453f5dc'
down_revision = '78f92d28db07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('followers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('follower_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['follower_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('followers', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('follower_id')

    # ### end Alembic commands ###