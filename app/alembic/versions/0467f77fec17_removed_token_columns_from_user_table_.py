"""removed token columns from user table, add tag column to resume table

Revision ID: 0467f77fec17
Revises: 8c91dce7f202
Create Date: 2022-03-18 10:37:07.330504

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0467f77fec17'
down_revision = '8c91dce7f202'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume', sa.Column('tag', sa.String(length=255), nullable=True))
    op.drop_index('ix_user_token', table_name='user')
    op.drop_column('user', 'token')
    op.drop_column('user', 'token_expiration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token_expiration', mysql.DATETIME(), nullable=True))
    op.add_column('user', sa.Column('token', mysql.VARCHAR(length=32), nullable=True))
    op.create_index('ix_user_token', 'user', ['token'], unique=False)
    op.drop_constraint(None, 'resume', type_='unique')
    op.drop_column('resume', 'tag')
    # ### end Alembic commands ###
