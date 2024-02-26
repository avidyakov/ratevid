import datetime
import decimal


class Repository:
    async def get_rate_by_codename(
        self, codename: str
    ) -> decimal.Decimal | None:
        raise NotImplementedError

    async def update_multi(self, codes_rates: dict) -> None:
        raise NotImplementedError

    async def get_last_update(self) -> datetime.datetime | None:
        raise NotImplementedError
