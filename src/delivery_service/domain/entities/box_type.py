from dataclasses import dataclass


@dataclass
class BoxType:
    """
    Box type entity.
    """

    id: int
    name: str | None = None
