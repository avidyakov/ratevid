import datetime
import decimal

from pydantic import BaseModel


class ExchangeInput(BaseModel):
    from_currency: str
    to_currency: str
    amount: decimal.Decimal


class ExchangeOutput(BaseModel):
    result: decimal.Decimal


class LastUpdateOutput(BaseModel):
    last_update: datetime.datetime | None
