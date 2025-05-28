from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from delivery_service.application.repositories.box_repository import \
    IBoxRepository
from delivery_service.domain.entities.box import Box
from delivery_service.domain.entities.box_type import BoxType
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.uuid import UUID
from delivery_service.infrastructure.sqlalchemy.models.box import BoxModel


class BoxRepository(IBoxRepository):
    """
    SQLAlchemy implementation of box repository.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, box: Box) -> None:
        """
        Adds a box to the repository.
        """
        box_model = BoxModel(
            id=str(box.id),
            user_id=str(box.user_id),
            box_type_id=box.box_type.id,
            weight=box.weight,
            name=box.name,
            price=box.price.value,
            price_currency=box.price.currency,
            delivery_price=box.delivery_price.value if box.delivery_price else None,
            delivery_currency=box.delivery_price.currency if box.delivery_price else None,
        )
        self._session.add(box_model)

    async def get(self, box_id: str) -> Box | None:
        """
        Gets a box by ID.
        """
        result = await self._session.execute(
            select(BoxModel).where(BoxModel.id == box_id)
        )
        box_model = result.scalar_one_or_none()
        if not box_model:
            return None

        return Box(
            id=UUID(box_model.id),
            user_id=UUID(box_model.user_id),
            name=box_model.name,
            box_type=BoxType(id=box_model.box_type_id),
            weight=box_model.weight,
            price=Money(box_model.price, box_model.price_currency),
            delivery_price=Money(box_model.delivery_price, box_model.delivery_currency) if box_model.delivery_price else None,
        )

    async def get_user_boxes(
        self,
        user_id: str,
        box_type_id: int | None = None,
        has_delivery_price: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Box]:
        """
        Gets user's boxes with optional filters and pagination.
        """
        query = select(BoxModel).where(BoxModel.user_id == user_id)

        if box_type_id is not None:
            query = query.where(BoxModel.box_type_id == box_type_id)

        if has_delivery_price is not None:
            if has_delivery_price:
                query = query.where(BoxModel.delivery_price.isnot(None))
            else:
                query = query.where(BoxModel.delivery_price.is_(None))

        query = query.limit(limit).offset(offset)
        result = await self._session.execute(query)
        box_models = result.scalars().all()

        return [
            Box(
                id=UUID(box_model.id),
                user_id=UUID(box_model.user_id),
                name=box_model.name,
                box_type=BoxType(id=box_model.box_type_id),
                weight=box_model.weight,
                price=Money(box_model.price, box_model.price_currency),
                delivery_price=Money(box_model.delivery_price, box_model.delivery_currency) if box_model.delivery_price else None,
            )
            for box_model in box_models
        ] 