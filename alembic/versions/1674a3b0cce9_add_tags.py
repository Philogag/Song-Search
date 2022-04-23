"""add tags

Revision ID: 1674a3b0cce9
Revises: 23fef7170283
Create Date: 2022-04-23 09:37:45.006212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1674a3b0cce9'
down_revision = '23fef7170283'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('st_songs_source', sa.Column('tags', sa.String(length=2000), nullable=True, comment='标签'))
    op.add_column('st_songs_source_history', sa.Column('tags', sa.String(length=2000), nullable=True, comment='标签'))
    op.add_column('st_songs_source_history', sa.Column('int_id', sa.Integer(), nullable=True, comment='数字id'))
    op.create_index(op.f('ix_st_songs_source_history_int_id'), 'st_songs_source_history', ['int_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_st_songs_source_history_int_id'), table_name='st_songs_source_history')
    op.drop_column('st_songs_source_history', 'int_id')
    op.drop_column('st_songs_source_history', 'tags')
    op.drop_column('st_songs_source', 'tags')
    # ### end Alembic commands ###
