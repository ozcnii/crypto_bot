"""new

Revision ID: f327413408db
Revises: bd58549a7bb4
Create Date: 2024-12-18 19:14:02.210860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f327413408db'
down_revision = 'bd58549a7bb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clans',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('peer', sa.Integer(), nullable=False),
    sa.Column('admin', sa.Integer(), nullable=False),
    sa.Column('users', sa.JSON(), nullable=False),
    sa.Column('league', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clans')
    # ### end Alembic commands ###
