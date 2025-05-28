import uuid
from dataclasses import dataclass

from delivery_service.domain.exceptions import InvalidBoxId


@dataclass(frozen=True)
class BoxId:
    """
    Unique identifier for a box.
    """

    value: uuid.UUID

    def __post_init__(self) -> None:
        """
        Validates that value is a UUID.
        """
        if not isinstance(self.value, uuid.UUID):
            raise InvalidBoxId(
                f"Expected UUID, got: {type(self.value).__name__}"
            )

    @staticmethod
    def new() -> "BoxId":
        """
        Generates a new BoxId.
        """
        return BoxId(uuid.uuid4())

    @staticmethod
    def from_str(value: str) -> "BoxId":
        """
        Creates BoxId from string.
        """
        return BoxId(uuid.UUID(value))

    def __str__(self) -> str:
        """
        Returns UUID as string.
        """
        return str(self.value)
