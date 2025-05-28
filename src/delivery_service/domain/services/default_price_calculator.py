from delivery_service.domain.entities.box import Box
from delivery_service.domain.exceptions import InvalidMoney
from delivery_service.domain.interfaces.delivery_price_calculator import (
    IDeliveryPriceCalculator,
)
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate
from delivery_service.domain.value_objects.money import Money


class DefaultPriceCalculator(IDeliveryPriceCalculator):
    def calculate(self, box: Box, exchange_rate: ExchangeRate) -> Money:
        """
        Default calculates delivery price.
        """
        if box.price.currency != exchange_rate.from_currency:
            raise InvalidMoney("Currency mismatch for exchange rate")

        # Вес в кг * 0.5 + цена в USD * 0.01, все в рублях
        return Money(
            value=(box.weight.value * 0.5 + box.price.value * 0.01)
            * exchange_rate.value,
            currency=exchange_rate.to_currency,
        )

