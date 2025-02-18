"""Add user status

Revision ID: e9af05f3ffbe
Revises: e8d4df4ac6e7
Create Date: 2025-02-18 22:11:55.985659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9af05f3ffbe'
down_revision: Union[str, None] = 'e8d4df4ac6e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE user_status AS ENUM ('active', 'inactive');")
    op.add_column(
        "users",
        sa.Column(
            "status",
            sa.Enum("active", "inactive", name="user_status"),
            nullable=True,
            default="active",
        ),
    )
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")
    op.alter_column("users", "status", nullable=False)


def downgrade() -> None:
    op.drop_column("users", "status")
    op.execute("DROP TYPE IF EXISTS user_status;")
