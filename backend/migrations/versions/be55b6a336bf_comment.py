"""<comment>

Revision ID: be55b6a336bf
Revises: 0ca7851a8850
Create Date: 2024-12-16 18:57:15.514188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be55b6a336bf'
down_revision = '0ca7851a8850'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('boosters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('types', sa.JSON(), nullable=False),
    sa.Column('prices', sa.JSON(), nullable=False),
    sa.Column('profits', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('xboosters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', sa.String(length=64), nullable=False),
    sa.Column('dateactivate', sa.String(length=64), nullable=False),
    sa.Column('timeout', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('xboostersinfo', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('xboostersinfo')

    op.drop_table('xboosters')
    op.drop_table('boosters')
    # ### end Alembic commands ###