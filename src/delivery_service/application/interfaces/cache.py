from typing import Any

from typing_extensions import Protocol


class ICache(Protocol):
    """
    Cache interface for set and get data.
    """

    async def set(self, key: str, value: Any, ttl: int) -> Any | None:
        """
        Set a value with time-to-live.
        """
        ...

    async def get(self, key: str) -> Any | None:
        """
        Get a value by key.
        """
        ...
