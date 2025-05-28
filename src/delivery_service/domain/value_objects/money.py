from dataclasses import dataclass

from delivery_service.domain.exceptions import InvalidMoney
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate


@dataclass(frozen=True)
class Money:
    """
    Represents money with value and currency.
    """

    value: float
    currency: Currency

    def __post_init__(self) -> None:
        """
        Validates value is non-negative.
        """
        if self.value < 0:
            raise InvalidMoney("Money value cannot be negative")

    def __add__(self, other: "Money") -> "Money":
        """
        Adds two amounts in the same currency.
        """
        if self.currency is not other.currency:
            raise InvalidMoney("Cannot add Money with different currencies")
        return Money(self.value + other.value, currency=self.currency)

    def to_currency(self, exchange_rate: "ExchangeRate") -> "Money":
        """
        Converts money to another currency using exchange rate.
        """
        if self.currency != exchange_rate.from_currency:
            raise InvalidMoney(
                f"Cannot convert Money from {self.currency} using exchange rate from {exchange_rate.from_currency}"
            )
        new_value = self.value * exchange_rate.value
        return Money(new_value, exchange_rate.to_currency)

    def __str__(self) -> str:
        """
        Returns money as a formatted string.
        """
        return f"{self.value:.2f} {self.currency.value}"
