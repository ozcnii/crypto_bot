"""new

Revision ID: 7d5649e96fcd
Revises: 3475cf740bee
Create Date: 2024-12-13 02:32:12.552374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d5649e96fcd'
down_revision = '3475cf740bee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('balance',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('balance',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
