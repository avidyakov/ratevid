import datetime
import decimal

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models import Currency
from services.repo.base import Repository


class RepositoryDB(Repository):
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def get_rate_by_codename(
        self, codename: str
    ) -> decimal.Decimal | None:
        return getattr(await self.db.get(Currency, codename), "rate", None)

    async def update_multi(self, data: dict) -> None:
        now = datetime.datetime.utcnow()
        insert_table = insert(Currency).values(
            [
                {
                    "codename": key,
                    "rate": str(value),
                    "updated_at": now,
                }
                for key, value in data.items()
            ]
        )
        insert_table_sql = insert_table.on_conflict_do_update(
            index_elements=("codename",),
            set_={
                "rate": insert_table.excluded.rate,
                "updated_at": insert_table.excluded.updated_at,
            },
        )
        await self.db.execute(insert_table_sql)
        await self.db.commit()

    async def get_last_update(self) -> datetime.datetime | None:
        query = select(Currency.updated_at).order_by(
            Currency.updated_at.desc()
        )
        result = await self.db.execute(query)
        return result.scalar()
