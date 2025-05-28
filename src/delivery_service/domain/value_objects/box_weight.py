from dataclasses import dataclass

from delivery_service.domain.exceptions import InvalidWeight


@dataclass(frozen=True)
class BoxWeight:
    """
    Box weight in kg.
    """

    value: float

    def __post_init__(self) -> None:
        """
        Validates is positive.
        """
        if self.value <= 0:
            raise InvalidWeight("Box Weight cannot be negative")
