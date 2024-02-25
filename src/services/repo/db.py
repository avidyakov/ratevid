import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Currency
from services.repo.base import Repository


class RepositoryDB(Repository):
    async def get_by_codename(self, db: AsyncSession, codename):
        return await db.get(Currency, codename)

    async def update_multi(self, db: AsyncSession, data: dict) -> None:
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
        await db.execute(insert_table_sql)
        await db.commit()

    async def get_last_update(self, db: AsyncSession) -> datetime.datetime:
        query = select(Currency.updated_at).order_by(
            Currency.updated_at.desc()
        )
        result = await db.execute(query)
        return result.scalar()
