"""empty message

Revision ID: 02378ef10974
Revises: b4b963c407e3
Create Date: 2016-02-04 11:02:33.140092

"""

# revision identifiers, used by Alembic.
revision = '02378ef10974'
down_revision = 'b4b963c407e3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_tag',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=True),
    sa.Column('slug', sa.String(length=60), nullable=True),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('added', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_blog_tag_slug'), 'blog_tag', ['slug'], unique=True)
    op.create_index(op.f('ix_blog_tag_name'), 'blog_tag', ['name'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_tag_name'), table_name='blog_tag')
    op.drop_index(op.f('ix_blog_tag_slug'), table_name='blog_tag')
    op.drop_table('blog_tag')
    ### end Alembic commands ###
