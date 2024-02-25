import logging
from http import HTTPStatus

import aiohttp

logger = logging.getLogger(__name__)


class ExchangeProviderError(Exception):
    pass


class BaseExchangeProvider:
    async def get_rates(self) -> dict:
        response_data = await self._fetch_data()
        return self._extract_rates(response_data)

    async def _fetch_data(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self._get_url()) as response:
                if response.status != HTTPStatus.OK:
                    raise ExchangeProviderError(
                        f"Error while getting data "
                        f"from {self._get_url()}: {response.status}"
                    )

                try:
                    data = await response.json()
                    logger.info(
                        f"Successfully fetched data from {self._get_url()}"
                    )
                    return data
                except aiohttp.ContentTypeError:
                    raise ExchangeProviderError(
                        f"Error while getting data "
                        f"from {self._get_url()}: {response.status}"
                    )

    def _get_url(self) -> str:
        raise NotImplementedError

    def _extract_rates(self, response_data: dict) -> dict:
        raise NotImplementedError
