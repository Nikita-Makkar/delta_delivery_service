from delivery_service.application.repositories.box_type_repository import \
    IBoxTypeRepository
from delivery_service.domain.entities.box_type import BoxType
from delivery_service.infrastructure.sqlalchemy.models.box_type import \
    BoxTypeModel
from delivery_service.infrastructure.sqlalchemy.repositories.repository import \
    SQLAlchemyRepository


class BoxTypeRepository(
    SQLAlchemyRepository[BoxType, BoxTypeModel], IBoxTypeRepository
):
    """
    SQLAlchemy repository for box types.
    """

    _model_class: type[BoxTypeModel] = BoxTypeModel

    def _model_to_entity(self, model: BoxTypeModel) -> BoxType:
        """
        Maps ORM model to domain entity.
        """
        return BoxType(
            id=model.id,
            name=model.name,
        )

    def _entity_to_model(self, entity: BoxType) -> BoxTypeModel:
        """
        Maps domain entity to ORM model.
        """
        return BoxTypeModel(
            id=entity.id,
            name=entity.name,
        )
