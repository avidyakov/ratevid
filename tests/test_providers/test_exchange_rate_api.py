import pytest

from services.rate_providers.exchange_rate_api import ExchangeRateAPIProvider


class TestExchangeRateAPIProvider:
    @pytest.fixture
    def sut(self):
        return ExchangeRateAPIProvider()

    @pytest.mark.asyncio
    async def test_get_rates(self, sut):
        rates = await sut.get_rates()

        assert len(rates) > 0
        assert rates["USD"] == 1
