from delivery_service.application.exceptions import (ApplicationError,
                                                     DatabaseException)
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.box_type_repository import \
    IBoxTypeRepository
from delivery_service.domain.entities.box_type import BoxType


class GetBoxTypesUseCase:
    """
    Use case for fetching all box types.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        repository: type[IBoxTypeRepository],
        logger: ILogger,
    ):
        self._repository: type[IBoxTypeRepository] = repository
        self._uow: IUnitOfWork = uow
        self._logger = logger

    async def __call__(self) -> list[BoxType]:
        """
        Returns list of all box types from repository.
        """
        try:
            self._logger.info("Requested list of box types")
            async with self._uow as uow:
                repository = self._repository(uow)
                result: list[BoxType] = await repository.find_all()
            return result
        except DatabaseException as e:
            self._logger.error(f"Failed to get box types: {e}")
            raise ApplicationError("Failed to get box types")
