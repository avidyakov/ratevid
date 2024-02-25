from core.config import app_settings
from services.rate_providers.base import (
    BaseExchangeProvider,
    ExchangeProviderError,
)


class ExchangeRateAPIProvider(BaseExchangeProvider):
    """ExchangeRate-API provider.
    https://www.exchangerate-api.com/docs/overview
    """

    def _extract_rates(self, response_data):
        try:
            return response_data["conversion_rates"]
        except KeyError:
            raise ExchangeProviderError(
                f"Error while extracting rates from response: {response_data}"
            )

    def _get_url(self):
        return app_settings.exchange_rate_api_url.format(
            api_key=app_settings.exchange_rate_api_key,
            base_currency=app_settings.base_currency,
        )
