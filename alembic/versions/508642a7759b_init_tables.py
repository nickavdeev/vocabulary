"""Init tables

Revision ID: 508642a7759b
Revises: 
Create Date: 2024-08-11 12:44:04.069887

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "508642a7759b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("telegram_id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.TIMESTAMP),
        sa.Column("updated_at", sa.TIMESTAMP),
    )

    op.create_table(
        "cards",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("telegram_id", sa.Integer, nullable=False),
        sa.Column("word", sa.TEXT, nullable=False),
        sa.Column("phase", sa.Integer, nullable=False, default=1),
        sa.Column(
            "next_repetition_on",
            sa.DATE,
            server_default=sa.func.current_date(),
        ),
        sa.Column(
            "status",
            sa.Enum("in_progress", "learned", name="card_status"),
            nullable=False,
            default="in_progress",
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(["telegram_id"], ["users.telegram_id"]),
    )


def downgrade() -> None:
    op.drop_table("cards")
    op.drop_table("users")
    op.execute("DROP TYPE card_status;")
