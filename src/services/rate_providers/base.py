from http import HTTPStatus

import aiohttp


class ExchangeProviderError(Exception):
    pass


class BaseExchangeProvider:
    async def get_rates(self):
        response_data = await self._fetch_data()
        return self._extract_rates(response_data)

    async def _fetch_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._get_url()) as response:
                if response.status != HTTPStatus.OK:
                    raise ExchangeProviderError(
                        f"Error while getting data "
                        f"from {self._get_url()}: {response.status}"
                    )

                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    raise ExchangeProviderError(
                        f"Error while getting data "
                        f"from {self._get_url()}: {response.status}"
                    )

    def _get_url(self):
        raise NotImplementedError
