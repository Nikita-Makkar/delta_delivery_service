from delivery_service.application.exceptions import (ApplicationError,
                                                     DatabaseException)
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.box_repository import \
    IBoxRepository
from delivery_service.domain.entities.box import Box


class GetUserBoxesUseCase:
    """
    Use case for fetching boxes by user.
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

    async def __call__(
        self,
        user_id: str,
        box_type_id: int | None = None,
        has_delivery_price: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Box]:
        """
        Returns filtered and paginated list of user's boxes.
        """
        try:
            self._logger.info(
                f"Requested list of box types from user {user_id} with filters: "
                f"box_type_id={box_type_id}, has_delivery_price={has_delivery_price}, "
                f"limit={limit}, offset={offset}"
            )
            async with self._uow as uow:
                repository = self._repository(uow)
                result: list[Box] = await repository.find_all_by_filters(
                    user_id, box_type_id, has_delivery_price, limit, offset
                )
            return result
        except DatabaseException as e:
            self._logger.error(f"Failed to get user boxes: {e}")
            raise ApplicationError("Failed to get user boxes")
