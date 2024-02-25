import decimal
import logging

logger = logging.getLogger(__name__)


def exchange(
    *,
    from_: decimal.Decimal,
    to: decimal.Decimal,
    amount: decimal.Decimal,
) -> decimal.Decimal:
    return round(amount / from_ * to, 2)


async def update_rates(provider, repo):
    logger.info(f"Starting to update rates from {provider.__class__.__name__}")
    rates = await provider.get_rates()
    await repo.update_multi(rates)
    logger.info(f"Finished updating rates from {provider.__class__.__name__}")
