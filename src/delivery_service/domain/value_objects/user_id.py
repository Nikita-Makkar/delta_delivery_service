import uuid
from dataclasses import dataclass

from delivery_service.domain.exceptions import InvalidUserId


@dataclass(frozen=True)
class UserId:
    """
    Unique identifier for a user.
    """

    value: uuid.UUID

    def __post_init__(self) -> None:
        """
        Validates that value is a UUID.
        """
        if not isinstance(self.value, uuid.UUID):
            raise InvalidUserId(f"Expected UUID, got {type(self.value)}")

    @staticmethod
    def new() -> "UserId":
        """
        Generates a new UserId.
        """
        return UserId(uuid.uuid4())

    @staticmethod
    def from_str(value: str) -> "UserId":
        """
        Parses UserId from string.
        """
        try:
            return UserId(uuid.UUID(value))
        except ValueError:
            raise InvalidUserId(f"Cannot parse {value} as UUID")

    def __str__(self) -> str:
        """
        Returns UUID as string.
        """
        return str(self.value)
