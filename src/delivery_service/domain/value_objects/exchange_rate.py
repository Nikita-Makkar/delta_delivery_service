from dataclasses import dataclass

from delivery_service.domain.exceptions import InvalidExchangeRate
from delivery_service.domain.value_objects.enums import Currency


@dataclass(frozen=True)
class ExchangeRate:
    """
    Exchange rate between two currencies.
    """

    value: float
    from_currency: Currency
    to_currency: Currency

    def __post_init__(self) -> None:
        if self.value < 0:
            raise InvalidExchangeRate("Exchange Rate value cannot be negative")
        elif self.value == 0:
            raise InvalidExchangeRate("Exchange Rate value cannot be zero")
