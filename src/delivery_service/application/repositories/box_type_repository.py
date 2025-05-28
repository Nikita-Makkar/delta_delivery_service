from typing import Protocol

from delivery_service.application.repositories.repository import IRepository
from delivery_service.domain.entities.box_type import BoxType


class IBoxTypeRepository(IRepository[BoxType], Protocol):
    """
    Repository interface for box types.
    """

    ...
