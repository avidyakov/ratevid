"""0001_init

Revision ID: b962bfaf22f0
Revises:
Create Date: 2024-02-24 16:13:56.157627

"""
import json
from pathlib import Path
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from src.models import Currency

# revision identifiers, used by Alembic.
revision: str = "b962bfaf22f0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currencies",
        sa.Column("codename", sa.String(), nullable=False),
        sa.Column("rate", sa.Numeric(), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("codename"),
        schema="app",
    )
    # ### end Alembic commands ###
    rates_path = Path(__file__).parent.parent / "fixtures/rates.json"
    rates = json.loads(rates_path.read_text())
    op.bulk_insert(Currency.__table__, rates)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("currencies", schema="app")
    # ### end Alembic commands ###
