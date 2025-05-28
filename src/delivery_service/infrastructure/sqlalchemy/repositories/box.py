from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from delivery_service.application.repositories.box_repository import \
    IBoxRepository
from delivery_service.domain.entities.box import Box
from delivery_service.domain.entities.box_type import BoxType
from delivery_service.domain.value_objects.box_id import BoxId
from delivery_service.domain.value_objects.box_weight import BoxWeight
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.user_id import UserId
from delivery_service.infrastructure.sqlalchemy.models.box import BoxModel
from delivery_service.infrastructure.sqlalchemy.repositories.repository import \
    SQLAlchemyRepository


class BoxRepository(
    SQLAlchemyRepository[Box, BoxModel], IBoxRepository
):
    """
    SQLAlchemy repository for managing boxes.
    """

    _model_class: type[BoxModel] = BoxModel

    def _model_to_entity(
        self, model: BoxModel, with_box_type_name: bool = False
    ) -> Box:
        """
        Maps ORM box model to domain entity.
        """
        return Box(
            id=BoxId.from_str(model.id),
            name=model.name,
            weight=BoxWeight(model.weight),
            box_type=BoxType(
                id=model.box_type_id,
                name=model.box_type.name if with_box_type_name else None,
            ),
            user_id=UserId.from_str(model.user_id),
            price=Money(model.price, Currency(model.price_currency)),
            delivery_price=(
                Money(model.delivery_price, Currency(model.delivery_currency))
                if model.delivery_price is not None
                else None
            ),
        )

    def _entity_to_model(self, entity: Box) -> BoxModel:
        """
        Maps domain box entity to ORM model.
        """
        return BoxModel(
            id=str(entity.id),
            name=entity.name,
            weight=entity.weight.value,
            box_type_id=entity.box_type.id,
            user_id=str(entity.user_id),
            price=entity.price.value,
            price_currency=entity.price.currency.value,
            delivery_price=(
                entity.delivery_price.value if entity.delivery_price else None
            ),
            delivery_currency=(
                entity.delivery_price.currency.value
                if entity.delivery_price
                else None
            ),
        )

    async def get_by_id(self, id: str) -> Box | None:
        """
        Returns box by ID with joined box type.
        """
        query = (
            select(self._model_class)
            .options(joinedload(self._model_class.box_type))
            .filter_by(id=id)
        )
        result = await self._session.execute(query)
        model = result.scalars().one_or_none()

        return (
            self._model_to_entity(model, with_box_type_name=True)
            if model
            else None
        )

    async def find_all_by_filters(
        self,
        user_id: str,
        box_type_id: int | None = None,
        has_delivery_price: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Box]:
        """
        Returns filtered and paginated list of boxes for a user.
        """
        query = (
            select(self._model_class)
            .options(joinedload(self._model_class.box_type))
            .where(self._model_class.user_id == user_id)
        )

        if box_type_id:
            query = query.where(
                self._model_class.box_type_id == box_type_id
            )

        if has_delivery_price is True:
            query = query.where(self._model_class.delivery_price.is_not(None))
        elif has_delivery_price is False:
            query = query.where(self._model_class.delivery_price.is_(None))

        query = query.limit(limit).offset(offset)

        result = await self._session.execute(query)
        models = result.scalars().all()

        return [
            self._model_to_entity(model, with_box_type_name=True)
            for model in models
        ]
