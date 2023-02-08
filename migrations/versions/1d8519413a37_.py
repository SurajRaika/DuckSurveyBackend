"""empty message

Revision ID: 1d8519413a37
Revises: a2361493c6b6
Create Date: 2023-01-22 17:41:08.280314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d8519413a37'
down_revision = 'a2361493c6b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('surveys', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('surveys', schema=None) as batch_op:
        batch_op.drop_column('img')

    # ### end Alembic commands ###