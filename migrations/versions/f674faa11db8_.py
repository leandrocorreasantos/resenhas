"""cliques from artigos

Revision ID: f674faa11db8
Revises: cfeef14e17db
Create Date: 2019-10-08 23:30:41.262563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f674faa11db8'
down_revision = 'cfeef14e17db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artigos', sa.Column(
        'cliques', sa.Integer(), nullable=True, server_default='0')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artigos', 'cliques')
    # ### end Alembic commands ###
