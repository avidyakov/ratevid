import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from schemas.currency import ExchangeInput, ExchangeOutput
from services.exchange import exchange
from services.rate_providers.exchange_rate_api import ExchangeRateAPIProvider
from services.repo.db import RepositoryDB

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/updates")
async def update_exchange_rates(
    provider: ExchangeRateAPIProvider = Depends(ExchangeRateAPIProvider),
    repo: RepositoryDB = Depends(RepositoryDB),
):
    rates = await provider.get_rates()
    await repo.update_multi(rates)
    logger.info("Rates updated")
    return ORJSONResponse(status_code=HTTPStatus.ACCEPTED, content={})


@router.get("/updates/last")
async def get_last_update(repo: RepositoryDB = Depends(RepositoryDB)):
    return {"last_update": await repo.get_last_update()}


@router.post(
    "/exchanges",
    response_model=ExchangeOutput,
)
async def execute_currency_exchange(
    exchange_input: ExchangeInput,
    repo: RepositoryDB = Depends(RepositoryDB),
):
    from_currency = await repo.get_by_codename(exchange_input.from_currency)
    if not from_currency:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="from_currency not found",
        )

    to_currency = await repo.get_by_codename(exchange_input.to_currency)
    if not to_currency:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY, detail="to_currency not found"
        )

    result = exchange(
        from_=from_currency.rate,
        to=to_currency.rate,
        amount=exchange_input.amount,
    )
    return ExchangeOutput(
        from_currency=exchange_input.from_currency,
        to_currency=exchange_input.to_currency,
        amount=exchange_input.amount,
        result=result,
    )
