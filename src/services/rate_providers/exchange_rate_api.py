import aiohttp

from services.rate_providers.base import ExchangeRateProvider


class ExchangeRateAPIProvider(ExchangeRateProvider):
    """ExchangeRate-API provider.
    https://www.exchangerate-api.com/docs/overview
    """

    async def get_rates(self):
        # make request with aiohttp
        async with aiohttp.ClientSession() as session:  # TODO: extract method
            async with session.get(
                "https://v6.exchangerate-api.com/"
                "v6/a9b5b6a88bfae857dabe764d/latest/USD"
            ) as response:  # TODO: use env var and base currency
                data = await response.json()  # TODO: handle errors
                return data["conversion_rates"]
