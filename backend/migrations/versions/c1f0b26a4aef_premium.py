"""premium

Revision ID: c1f0b26a4aef
Revises: ae7b8c469c57
Create Date: 2025-01-26 19:06:23.874854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f0b26a4aef'
down_revision = 'ae7b8c469c57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('premium', sa.Integer(), server_default=sa.text('0'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('premium')

    # ### end Alembic commands ###
