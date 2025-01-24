"""token

Revision ID: 198b224017de
Revises: f327413408db
Create Date: 2025-01-23 19:59:39.944318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '198b224017de'
down_revision = 'f327413408db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('token')

    # ### end Alembic commands ###