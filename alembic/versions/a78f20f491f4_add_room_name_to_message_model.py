"""Add room_name to Message model

Revision ID: a78f20f491f4
Revises: 773b8ce9ab60
Create Date: 2025-07-10 19:23:07.525176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a78f20f491f4'
down_revision: Union[str, Sequence[str], None] = '773b8ce9ab60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('room_name', sa.String(length=255), server_default=sa.text("Stovi's Chatroom"), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'room_name')
    # ### end Alembic commands ###
