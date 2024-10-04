"""empty message

Revision ID: f74cac455736
Revises: 5ff4b519585c
Create Date: 2024-10-04 20:33:55.904745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74cac455736'
down_revision = '5ff4b519585c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testimonials',
    sa.Column('testimonial_id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=255), nullable=False),
    sa.Column('body', sa.LargeBinary(), nullable=False),
    sa.Column('company', sa.String(length=255), nullable=True),
    sa.Column('imageurl', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('Published', 'Pending', 'Deleted', name='status'), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('testimonial_id')
    )
    op.create_table('sliders',
    sa.Column('slider_id', sa.Integer(), nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('subtitle', sa.String(length=255), nullable=True),
    sa.Column('body', sa.LargeBinary(), nullable=True),
    sa.Column('imageurl', sa.String(length=255), nullable=False),
    sa.Column('link1', sa.String(length=255), nullable=True),
    sa.Column('link2', sa.String(length=255), nullable=True),
    sa.Column('sliderstatus', sa.Enum('Published', 'Pending', 'Deleted', name='sliderstatus'), nullable=False),
    sa.Column('align', sa.Enum('Left', 'Center', 'Right', name='slideralign'), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['page_id'], ['pages.page_id'], ),
    sa.PrimaryKeyConstraint('slider_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sliders')
    op.drop_table('testimonials')
    # ### end Alembic commands ###