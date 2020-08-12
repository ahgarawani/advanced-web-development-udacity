"""empty message

Revision ID: 28be6664d16e
Revises: 
Create Date: 2020-08-13 00:51:44.415202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28be6664d16e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))

    op.execute('UPDATE todos SET completed = False WHERE completed is NULL;')

    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
