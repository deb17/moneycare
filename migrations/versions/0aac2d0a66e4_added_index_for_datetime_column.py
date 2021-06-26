"""Added index for datetime column

Revision ID: 0aac2d0a66e4
Revises: 26e24938c75b
Create Date: 2021-05-30 08:26:22.156627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aac2d0a66e4'
down_revision = '26e24938c75b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_expenses_updated_on'), 'expenses', ['updated_on'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_expenses_updated_on'), table_name='expenses')
    # ### end Alembic commands ###