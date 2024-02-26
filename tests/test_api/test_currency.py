from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest

from services.rate_providers.exchange_rate_api import ExchangeRateAPIProvider
from src.models import Currency


@patch.object(ExchangeRateAPIProvider, "get_rates", new_callable=AsyncMock)
def test_task_update_initiated(mock_get_rates, client, session):
    mock_get_rates.return_value = {
        "USD": 1,
        "EUR": 0.85,
        "GBP": 0.75,
    }

    response = client.post("/api/updates")
    assert response.status_code == HTTPStatus.ACCEPTED

    currency = session.get(Currency, "USD")
    assert currency.rate == 1

    currency = session.get(Currency, "EUR")
    assert currency.rate == 0.85

    currency = session.get(Currency, "GBP")
    assert currency.rate == 0.75


@pytest.mark.asyncio
def test_exchange_currency(client, session):
    user = session.get(Currency, "EUR")
    user.rate = 0.85
    session.commit()

    response = client.post(
        "/api/exchanges",
        json={"from_currency": "USD", "to_currency": "EUR", "amount": 100},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"result": "85.00"}
