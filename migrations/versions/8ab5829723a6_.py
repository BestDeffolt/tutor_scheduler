"""empty message

Revision ID: 8ab5829723a6
Revises: 88acc09dddcf
Create Date: 2023-05-09 18:39:28.401865

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8ab5829723a6'
down_revision = '88acc09dddcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.alter_column('prefer_start_time',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Time(),
               existing_nullable=True)
        batch_op.alter_column('prefer_end_time',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Time(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.alter_column('prefer_end_time',
               existing_type=sa.Time(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
        batch_op.alter_column('prefer_start_time',
               existing_type=sa.Time(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)

    # ### end Alembic commands ###