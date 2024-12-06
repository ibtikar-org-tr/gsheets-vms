"""Initial migration

Revision ID: 64a8a78a1cd4
Revises: 
Create Date: 2024-12-06 21:38:35.493366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '64a8a78a1cd4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sheet',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('sheetID', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('last_sent', sa.DateTime(), nullable=True),
    sa.Column('sheetID', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('projectName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pageID', sa.Integer(), nullable=False),
    sa.Column('row_number', sa.Integer(), nullable=False),
    sa.Column('ownerID', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('ownerName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('ownerEmail', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('ownerPhone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('managerName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('taskText', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('priority', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dueDate', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('blocked_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('milestone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('sheet')
    # ### end Alembic commands ###