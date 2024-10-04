"""empty message

Revision ID: a754ae96410b
Revises: 0f9ed2a6f8f7
Create Date: 2024-10-04 20:31:36.583527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a754ae96410b'
down_revision = '0f9ed2a6f8f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pages',
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.Column('pagetitle', sa.String(length=100), nullable=False),
    sa.Column('pageslug', sa.String(length=100), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('metakeyword', sa.Text(), nullable=True),
    sa.Column('metadesc', sa.Text(), nullable=True),
    sa.Column('pagestatus', sa.Enum('PUBLISHED', 'PENDING', 'DELETED', name='pagestatus'), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('page_id'),
    sa.UniqueConstraint('pageslug'),
    sa.UniqueConstraint('pagetitle')
    )
    op.create_table('sections',
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('sectiontitle', sa.String(length=255), nullable=False),
    sa.Column('sectionslug', sa.String(length=255), nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.Column('sectionintro', sa.LargeBinary(), nullable=True),
    sa.Column('sectionbody', sa.LargeBinary(), nullable=False),
    sa.Column('sectionicon', sa.String(length=100), nullable=True),
    sa.Column('extlink', sa.String(length=255), nullable=True),
    sa.Column('sectionstatus', sa.Enum('PUBLISHED', 'PENDING', 'DELETED', name='sectionstatus'), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['page_id'], ['pages.page_id'], ),
    sa.PrimaryKeyConstraint('section_id'),
    sa.UniqueConstraint('sectionslug'),
    sa.UniqueConstraint('sectiontitle')
    )
    op.create_table('sectiondocs',
    sa.Column('sectiondoc_id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('docurl', sa.String(length=255), nullable=False),
    sa.Column('doctype', sa.Enum('IMAGE', 'VIDEO', 'AUDIO', 'PDF', 'OTHERS', name='doctype'), nullable=False),
    sa.Column('sectiondocstatus', sa.Enum('PUBLISHED', 'PENDING', 'DELETED', name='sectiondocstatus'), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['sections.section_id'], ),
    sa.PrimaryKeyConstraint('sectiondoc_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sectiondocs')
    op.drop_table('sections')
    op.drop_table('pages')
    # ### end Alembic commands ###
