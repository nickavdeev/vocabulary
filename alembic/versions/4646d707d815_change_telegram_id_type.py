"""Change telegram_id type

Revision ID: 4646d707d815
Revises: e9af05f3ffbe
Create Date: 2025-09-04 12:55:34.680659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4646d707d815'
down_revision: Union[str, None] = 'e9af05f3ffbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "telegram_id",
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.alter_column(
        "cards",
        "telegram_id",
        type_=sa.BigInteger(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "cards",
        "telegram_id",
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "telegram_id",
        type_=sa.Integer(),
        existing_nullable=False,
    )
