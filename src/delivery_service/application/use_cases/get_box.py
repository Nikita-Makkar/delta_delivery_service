from delivery_service.application.exceptions import (ApplicationError,
                                                     BoxNotFoundError,
                                                     DatabaseException)
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.box_repository import \
    IBoxRepository
from delivery_service.domain.entities.box import Box


class GetBoxUseCase:
    """
    Use case for fetching a box by ID.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        repository: type[IBoxRepository],
        logger: ILogger,
    ):
        self._repository: type[IBoxRepository] = repository
        self._uow: IUnitOfWork = uow
        self._logger = logger

    async def __call__(self, box_id: int) -> Box:
        """
        Returns box by ID or raises error if not found.
        """
        try:
            self._logger.info(f"Requested info of box: {box_id}")
            async with self._uow as uow:
                repository = self._repository(uow)
                result = await repository.get_by_id(box_id)
        except DatabaseException as e:
            self._logger.error(f"Failed to get box: {e}")
            raise ApplicationError("Failed to get box")

        if result is None:
            raise BoxNotFoundError(f"Box with id {box_id} not found")

        return result
