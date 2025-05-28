from typing_extensions import Protocol

from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate


class IExchangeRate(Protocol):
    """
    Interface for fetching currency exchange rates.
    """

    async def get_rate(
        self, from_currency: Currency, to_currency: Currency
    ) -> ExchangeRate:
        """
        Returns exchange rate between two currencies.
        """
        ...
