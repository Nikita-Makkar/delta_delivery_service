from typing import Any, Protocol

from delivery_service.application.repositories.repository import IRepository
from delivery_service.domain.entities.box import Box


class IBoxRepository(IRepository[Box], Protocol):
    """
    Repository interface for boxes.
    """

    async def find_all_by_filters(self, **filter_by: Any) -> list[Box]:
        """
        Returns boxes matching given filters.
        """
        ...
