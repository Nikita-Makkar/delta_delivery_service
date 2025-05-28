from typing import Protocol

from delivery_service.domain.entities.box import Box
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate
from delivery_service.domain.value_objects.money import Money


class IDeliveryPriceCalculator(Protocol):
    """
    Interface for calculating delivery price.
    """

    def calculate_price(
        self, box: Box, exchange_rate: ExchangeRate
    ) -> Money: ...
