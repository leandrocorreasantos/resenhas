"""empty message

Revision ID: c238f53b4e83
Revises: a89e624968ef
Create Date: 2019-11-04 07:34:16.066893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c238f53b4e83'
down_revision = 'a89e624968ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'artigos', sa.Column(
            'meta_description', sa.String(length=255), nullable=True
        )
    )
    op.add_column(
        'artigos', sa.Column(
            'meta_keywords', sa.String(length=100), nullable=True
        )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artigos', 'meta_keywords')
    op.drop_column('artigos', 'meta_description')
    # ### end Alembic commands ###
