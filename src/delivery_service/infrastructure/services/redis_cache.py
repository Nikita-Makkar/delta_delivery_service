import json
from typing import Any

import redis.asyncio as redis

from delivery_service.application.interfaces.cache import ICache
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.infrastructure.config import settings


class RedisCache(ICache):
    """
    Redis implementation of the ICache interface.
    """

    def __init__(
        self,
        logger: ILogger,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
    ):
        self._redis = redis.Redis(host=host, port=port, decode_responses=True)
        self._logger = logger

    async def get(self, key: str) -> Any | None:
        """
        Gets cached value from Redis by key.
        """
        try:
            data = await self._redis.get(key)
            result = json.loads(data) if data else None
            if result:
                self._logger.info(
                    f"Get cached data for key {key}:{result} from Redis"
                )
            return result
        except Exception as e:
            self._logger.error(f"Failed Redis read for key {key}: {e}")
            return None

    async def set(
        self, key: str, value: Any, ttl: int = settings.REDIS_TTL
    ) -> None:
        """
        Sets value in Redis with TTL.
        """
        try:
            json_data = json.dumps(value)
            await self._redis.set(key, json_data, ex=ttl)
            self._logger.info(
                f"Set data for key {key}:{json_data} in Redis with TTL {ttl}"
            )
        except Exception as e:
            self._logger.error(
                f"Failed Redis write for key {key} with value {value}: {e}"
            )
