from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from delivery_service.application.exceptions import SessionNotProvidedException
from delivery_service.application.repositories.repository import IRepository
from delivery_service.infrastructure.sqlalchemy.database import Base
from delivery_service.infrastructure.sqlalchemy.unit_of_work import \
    SQLAlchemyUnitOfWork

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel", bound=Base)


class SQLAlchemyRepository(
    ABC, IRepository[TEntity], Generic[TEntity, TModel]
):
    """
    Base SQLAlchemy repository.
    """

    _model_class: type[TModel]

    def __init__(self, uow: SQLAlchemyUnitOfWork):
        if not uow.session:
            raise SessionNotProvidedException("Session is not initialized")
        self._session: AsyncSession = uow.session

    @abstractmethod
    def _model_to_entity(self, model: TModel) -> TEntity:
        """
        Converts ORM model to domain entity.
        """
        raise NotImplementedError

    @abstractmethod
    def _entity_to_model(self, entity: TEntity) -> TModel:
        """
        Converts domain entity to ORM model.
        """
        raise NotImplementedError

    async def add(self, entity: TEntity) -> TEntity | None:
        """
        Adds entity to database and returns it.
        """
        model = self._entity_to_model(entity)
        self._session.add(model)
        await self._session.flush()
        return self._model_to_entity(model)

    async def get_by_id(self, id: int) -> TEntity | None:
        """
        Retrieves entity by ID or returns None.
        """
        result: Result[tuple[TModel]] = await self._session.execute(
            select(self._model_class).filter_by(id=id)
        )
        model = result.scalars().one_or_none()
        return self._model_to_entity(model) if model else None

    async def find_all(
        self,
        **filter_by: Any,
    ) -> list[TEntity]:
        """
        Finds all entities matching filter.
        """
        query = select(self._model_class).filter_by(**filter_by)

        result: Result[tuple[TModel]] = await self._session.execute(query)

        model_list: list[TModel] = list(result.scalars().all())
        return [self._model_to_entity(model) for model in model_list]
