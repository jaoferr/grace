"""added batch, job, tag tables

Revision ID: 7c6ef42baf85
Revises: 0467f77fec17
Create Date: 2022-03-18 14:12:52.525307

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7c6ef42baf85'
down_revision = '0467f77fec17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batch',
    sa.Column('id', sa.String(length=24), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item_count', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_batch_id'), 'batch', ['id'], unique=True)
    op.create_index(op.f('ix_batch_timestamp'), 'batch', ['timestamp'], unique=False)
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=True)
    op.create_table('resumetag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('tag', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resumetag_id'), 'resumetag', ['id'], unique=True)
    op.create_index(op.f('ix_resumetag_tag'), 'resumetag', ['tag'], unique=True)
    op.add_column('resume', sa.Column('tag_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'resume', 'batch', ['batch_id'], ['id'])
    op.create_foreign_key(None, 'resume', 'resumetag', ['tag_id'], ['id'])
    op.drop_column('resume', 'tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume', sa.Column('tag', mysql.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'resume', type_='foreignkey')
    op.drop_constraint(None, 'resume', type_='foreignkey')
    op.drop_column('resume', 'tag_id')
    op.drop_index(op.f('ix_resumetag_tag'), table_name='resumetag')
    op.drop_index(op.f('ix_resumetag_id'), table_name='resumetag')
    op.drop_table('resumetag')
    op.drop_index(op.f('ix_jobs_id'), table_name='jobs')
    op.drop_table('jobs')
    op.drop_index(op.f('ix_batch_timestamp'), table_name='batch')
    op.drop_index(op.f('ix_batch_id'), table_name='batch')
    op.drop_table('batch')
    # ### end Alembic commands ###
