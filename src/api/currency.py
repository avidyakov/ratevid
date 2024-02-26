import asyncio
import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from schemas.currency import ExchangeInput, ExchangeOutput, LastUpdateOutput
from services.exchange import exchange, update_rates
from services.rate_providers.exchange_rate_api import ExchangeRateAPIProvider
from services.repo.db import RepositoryDB

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/updates")
async def update_exchange_rates(
    provider: ExchangeRateAPIProvider = Depends(ExchangeRateAPIProvider),
    repo: RepositoryDB = Depends(RepositoryDB),
):
    asyncio.create_task(update_rates(provider, repo))
    logger.info("Rates update initiated")
    return ORJSONResponse(status_code=HTTPStatus.ACCEPTED, content={})


@router.get("/updates/last", response_model=LastUpdateOutput)
async def get_last_update(repo: RepositoryDB = Depends(RepositoryDB)):
    return LastUpdateOutput(last_update=await repo.get_last_update())


@router.post(
    "/exchanges",
    response_model=ExchangeOutput,
)
async def execute_currency_exchange(
    exchange_input: ExchangeInput,
    repo: RepositoryDB = Depends(RepositoryDB),
):
    from_currency = await repo.get_rate_by_codename(
        exchange_input.from_currency
    )
    if not from_currency:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="from_currency not found",
        )

    to_currency = await repo.get_rate_by_codename(exchange_input.to_currency)
    if not to_currency:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="to_currency not found",
        )

    result = exchange(
        from_=from_currency,
        to=to_currency,
        amount=exchange_input.amount,
    )
    return ExchangeOutput(result=result)
