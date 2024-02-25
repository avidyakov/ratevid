import datetime

from models import Currency


class Repository:
    async def get_by_codename(self, codename: str) -> Currency | None:
        raise NotImplementedError

    async def update_multi(self, codes_rates: dict) -> None:
        raise NotImplementedError

    async def get_last_update(self) -> datetime.datetime | None:
        raise NotImplementedError
