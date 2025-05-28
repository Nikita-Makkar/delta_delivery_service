from uuid import uuid4

from fastapi import APIRouter, Depends, Query, Response

from delivery_service.application.dto.box import BoxDTO
from delivery_service.application.use_cases.get_box import GetBoxUseCase
from delivery_service.application.use_cases.get_box_types import \
    GetBoxTypesUseCase
from delivery_service.application.use_cases.get_user_boxes import \
    GetUserBoxesUseCase
from delivery_service.domain.entities.box import Box
from delivery_service.domain.entities.box_type import BoxType
from delivery_service.infrastructure.rabbitmq.producer import BoxProducer
from delivery_service.presentation.dependencies.box import (get_box_producer,
                                                            get_box_types_uc,
                                                            get_box_uc,
                                                            get_user_boxes_uc)
from delivery_service.presentation.dependencies.user import \
    get_user_id_from_cookie
from delivery_service.presentation.mappers.box import (map_entity_to_response,
                                                       map_register_to_dto)
from delivery_service.presentation.schemas.box import BoxResponse
from delivery_service.presentation.schemas.box_type import BoxTypeResponse
from delivery_service.presentation.schemas.register_box import (
    RegisterBox, RegisterBoxResponse)

router = APIRouter(prefix="/boxes", tags=["Boxes"])


@router.post("/")
async def register_box(
    box_dto: RegisterBox,
    response: Response,
    user_id: str | None = Depends(get_user_id_from_cookie),
    box_producer: BoxProducer = Depends(get_box_producer),
) -> RegisterBoxResponse:
    """
    Registers a new box with RabbitMQ and sets user cookie.
    """
    if not user_id:
        user_id = str(uuid4())
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            samesite="lax",
            max_age=86400 * 30,
        )

    box_dto: BoxDTO = map_register_to_dto(box_dto, user_id)
    await box_producer.publish(box_dto)
    return RegisterBoxResponse(box_id=box_dto.box_id)


@router.get("/{box_id}")
async def get_box_info(
    box_id: str,
    get_box_uc: GetBoxUseCase = Depends(get_box_uc),
) -> BoxResponse:
    """
    Returns box details by ID.
    """
    box: Box = await get_box_uc(box_id)
    return map_entity_to_response(box)


@router.get("/")
async def get_user_boxes(
    box_type_id: int | None = Query(None),
    has_delivery_price: bool | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: str | None = Depends(get_user_id_from_cookie),
    get_user_box_uc: GetUserBoxesUseCase = Depends(get_user_boxes_uc),
) -> list[BoxResponse] | None:
    """
    Returns user's Boxes with optional filters and pagination.
    """
    if not user_id:
        return None

    boxes: list[Box] = await get_user_box_uc(
        user_id,
        box_type_id,
        has_delivery_price,
        limit,
        offset,
    )
    return [map_entity_to_response(b) for b in boxes]


@router.get("/types/")
async def get_box_types(
    get_box_types_uc: GetBoxTypesUseCase = Depends(get_box_types_uc),
) -> list[BoxTypeResponse]:
    """
    Returns box types.
    """
    result: list[BoxType] = await get_box_types_uc()
    return [BoxTypeResponse.model_validate(p) for p in result]
