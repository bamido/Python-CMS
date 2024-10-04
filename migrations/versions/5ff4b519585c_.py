"""empty message

Revision ID: 5ff4b519585c
Revises: a754ae96410b
Create Date: 2024-10-04 20:33:14.368264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ff4b519585c'
down_revision = 'a754ae96410b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('tagname', sa.String(length=255), nullable=False),
    sa.Column('tagslug', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('tagname'),
    sa.UniqueConstraint('tagslug')
    )
    op.create_table('threads',
    sa.Column('thread_id', sa.Integer(), nullable=False),
    sa.Column('threadname', sa.String(length=255), nullable=False),
    sa.Column('threadslug', sa.String(length=255), nullable=False),
    sa.Column('threadstatus', sa.Enum('Published', 'Pending', 'Deleted', name='threadstatus'), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('thread_id'),
    sa.UniqueConstraint('threadname'),
    sa.UniqueConstraint('threadslug')
    )
    op.create_table('posts',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('posttitle', sa.String(length=255), nullable=False),
    sa.Column('postslug', sa.String(length=255), nullable=False),
    sa.Column('thread_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('postintro', sa.LargeBinary(), nullable=True),
    sa.Column('postbody', sa.LargeBinary(), nullable=False),
    sa.Column('postimageurl', sa.String(length=255), nullable=True),
    sa.Column('postvideourl', sa.String(length=255), nullable=True),
    sa.Column('poststatus', sa.Enum('Published', 'Pending', 'Deleted', name='poststatus'), nullable=False),
    sa.Column('postview', sa.Integer(), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('metakeyword', sa.Text(), nullable=True),
    sa.Column('metadesc', sa.Text(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['thread_id'], ['threads.thread_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('post_id'),
    sa.UniqueConstraint('postslug'),
    sa.UniqueConstraint('posttitle')
    )
    op.create_table('posttags',
    sa.Column('posttag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.tag_id'], ),
    sa.PrimaryKeyConstraint('posttag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posttags')
    op.drop_table('posts')
    op.drop_table('threads')
    op.drop_table('tags')
    # ### end Alembic commands ###
