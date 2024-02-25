from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from schemas.currency import ExchangeInput, ExchangeOutput
from services.exchange import exchange
from services.rate_providers.exchange_rate_api import ExchangeRateAPIProvider
from services.repo.db import RepositoryDB

router = APIRouter()


@router.post("/updates")
async def update_exchange_rates(
    provider: ExchangeRateAPIProvider = Depends(ExchangeRateAPIProvider),
    repo: RepositoryDB = Depends(RepositoryDB),
):
    rates = await provider.get_rates()
    await repo.update_multi(rates)
    return ORJSONResponse(status_code=HTTPStatus.ACCEPTED, content={})


@router.get("/updates/last")
async def last_update(repo: RepositoryDB = Depends(RepositoryDB)):
    return {"last_update": await repo.get_last_update()}


@router.post(
    "/exchanges",
    response_model=ExchangeOutput,
)
async def exchange_currency(
    exchange_input: ExchangeInput,
    repo: RepositoryDB = Depends(RepositoryDB),
):
    result = exchange(
        from_=await repo.get_by_codename(exchange_input.from_currency),
        to=await repo.get_by_codename(exchange_input.to_currency),
        amount=exchange_input.amount,
    )
    return ExchangeOutput(
        from_currency=exchange_input.from_currency,
        to_currency=exchange_input.to_currency,
        amount=exchange_input.amount,
        result=result,
    )
