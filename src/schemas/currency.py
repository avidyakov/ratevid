import decimal

from pydantic import BaseModel


class ExchangeInput(BaseModel):
    from_currency: str
    to_currency: str
    amount: decimal.Decimal


class ExchangeOutput(ExchangeInput):
    result: decimal.Decimal
