from delivery_service.application.dto.box import BoxDTO
from delivery_service.domain.entities.box import Box
from delivery_service.domain.value_objects.box_id import BoxId
from delivery_service.presentation.schemas.box import BoxResponse
from delivery_service.presentation.schemas.register_box import RegisterBox


def map_register_to_dto(
    box_register: RegisterBox, user_id: str
) -> BoxDTO:
    """
    Converts registration scheme to BoxDTO.
    """
    return BoxDTO(
        box_id=str(BoxId.new()),
        user_id=user_id,
        name=box_register.name,
        weight=box_register.weight,
        box_type_id=box_register.box_type_id,
        price_usd=box_register.price_usd,
    )


def map_entity_to_response(entity: Box) -> BoxResponse:
    """
    Converts Box entity to response schema.
    """
    return BoxResponse(
        id=str(entity.id),
        name=entity.name,
        weight=entity.weight.value,
        box_type=entity.box_type.name,
        price_usd=round(entity.price.value, 2),
        delivery_price_rub=round(entity.delivery_price.value, 2)
        if entity.delivery_price
        else None,
    )
