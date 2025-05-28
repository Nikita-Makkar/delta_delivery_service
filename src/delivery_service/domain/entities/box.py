from dataclasses import dataclass

from delivery_service.domain.entities.box_type import BoxType
from delivery_service.domain.exceptions import DeliveryPriceAlreadySet
from delivery_service.domain.value_objects.box_id import BoxId
from delivery_service.domain.value_objects.box_weight import BoxWeight
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.user_id import UserId


@dataclass
class Box:
    """
    Box entity.
    """

    id: BoxId
    user_id: UserId
    name: str
    box_type: BoxType
    weight: BoxWeight
    price: Money
    delivery_price: Money | None = None

    def set_delivery_price(self, price: Money) -> None:
        """
        Set delivery price.
        """
        if self.delivery_price is not None:
            raise DeliveryPriceAlreadySet("Delivery price already set")
        self.delivery_price = price
