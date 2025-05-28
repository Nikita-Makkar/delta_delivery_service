from dataclasses import dataclass

from delivery_service.domain.entities.box import Box
from delivery_service.domain.entities.box_type import BoxType
from delivery_service.domain.value_objects.box_id import BoxId
from delivery_service.domain.value_objects.box_weight import BoxWeight
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.user_id import UserId


@dataclass
class BoxDTO:
    """
    DTO for box data transfer.
    """

    box_id: str
    user_id: str
    name: str
    weight: float
    box_type_id: int
    price_usd: float


def map_dto_to_entity(box_dto: BoxDTO) -> Box:
    """
    Mapping BoxDTO to Box entity.
    """
    return Box(
        id=BoxId.from_str(box_dto.box_id),
        user_id=UserId.from_str(box_dto.user_id),
        name=box_dto.name,
        box_type=BoxType(id=box_dto.box_type_id),
        weight=BoxWeight(box_dto.weight),
        price=Money(box_dto.price_usd, Currency.USD),
    )
