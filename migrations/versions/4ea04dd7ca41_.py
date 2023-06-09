"""empty message

Revision ID: 4ea04dd7ca41
Revises: e1f57922b989
Create Date: 2023-05-09 19:35:24.694048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ea04dd7ca41'
down_revision = 'e1f57922b989'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_form', schema=None) as batch_op:
        batch_op.add_column(sa.Column('day', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_form', schema=None) as batch_op:
        batch_op.drop_column('day')

    # ### end Alembic commands ###
