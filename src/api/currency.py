from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.currency import ExchangeInput, ExchangeOutput
from services.rate_providers.exchange_rate_api import ExchangeRateAPIProvider
from services.repo.db import RepositoryDB

router = APIRouter()


@router.post("/updates")
async def update_exchange_rates(db: AsyncSession = Depends(get_session)):
    rates = (
        await ExchangeRateAPIProvider().get_rates()
    )  # TODO: dependecy and execution in task
    repo = RepositoryDB()
    await repo.update_multi(db, rates)
    return ORJSONResponse(
        status_code=HTTPStatus.ACCEPTED,
        content=None,
    )


@router.get("/updates/last")
async def last_update(db: AsyncSession = Depends(get_session)):
    repo = RepositoryDB()  # TODO: dependecy
    last_update = await repo.get_last_update(db)
    return {"last_update": last_update}


@router.post(
    "/exchanges",
    response_model=ExchangeOutput,
)
async def exchange_currency(
    exchange_input: ExchangeInput, db: AsyncSession = Depends(get_session)
):
    repo = RepositoryDB()
    from_currency = await repo.get_by_codename(
        db, exchange_input.from_currency
    )
    to_currency = await repo.get_by_codename(db, exchange_input.to_currency)
    result = round(  # TODO: exract to service
        exchange_input.amount / from_currency.rate * to_currency.rate, 2
    )
    return ExchangeOutput(
        from_currency=exchange_input.from_currency,
        to_currency=exchange_input.to_currency,
        amount=exchange_input.amount,
        result=result,
    )
