"""Add idPlace to favorite

Revision ID: b88fadc963ef
Revises: <previous_revision_id>
Create Date: 2024-11-18

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b88fadc963ef'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Comando para añadir la columna 'idPlace' a la tabla 'favorite'
    op.add_column('favorite', sa.Column('idPlace', sa.String(), nullable=False, server_default=''))

def downgrade():
    # Comando para eliminar la columna 'idPlace' si se hace rollback
    op.drop_column('favorite', 'idPlace')
