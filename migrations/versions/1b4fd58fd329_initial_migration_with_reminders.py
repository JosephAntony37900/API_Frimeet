"""Add reminders columns to user

Revision ID: <revision_id>
Revises: <previous_revision_id>
Create Date: <current_date>

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1b4fd58fd329'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('eventReminder', postgresql.ARRAY(sa.String()), nullable=True), schema='multidisciplinario')
    op.add_column('users', sa.Column('ContentReminder', postgresql.ARRAY(sa.String()), nullable=True), schema='multidisciplinario')
    op.add_column('users', sa.Column('nameReminder', postgresql.ARRAY(sa.String()), nullable=True), schema='multidisciplinario')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'eventReminder', schema='multidisciplinario')
    op.drop_column('users', 'ContentReminder', schema='multidisciplinario')
    op.drop_column('users', 'nameReminder', schema='multidisciplinario')
    # ### end Alembic commands ###
