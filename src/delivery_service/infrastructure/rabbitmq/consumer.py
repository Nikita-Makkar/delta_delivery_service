import json

import aio_pika

from delivery_service.application.dto.box import BoxDTO, map_dto_to_entity
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.use_cases.register_box import \
    RegisterBoxUseCase
from delivery_service.infrastructure.config import settings


class BoxConsumer:
    """
    Consumes box registration messages from RabbitMQ.
    """

    def __init__(
        self,
        register_box_uc: RegisterBoxUseCase,
        logger: ILogger,
        rabbitmq_url: str = settings.RABBITMQ_URL,
        queue_name: str = "register_box",
    ):
        self._rabbitmq_url: str = rabbitmq_url
        self._queue_name: str = queue_name
        self._register_box_uc: RegisterBoxUseCase = register_box_uc
        self._logger = logger

    async def start(self) -> None:
        """
        Listens to RabbitMQ queue and registers incoming boxes.
        """
        try:
            self._logger.info("[BoxConsumer] Connecting to RabbitMQ...")
            connection = await aio_pika.connect_robust(self._rabbitmq_url)
            channel = await connection.channel()
            queue = await channel.declare_queue(self._queue_name, durable=True)
            self._logger.info(
                f"[BoxConsumer] Waiting for messages on queue: {self._queue_name}"
            )
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    self._logger.info(
                        "[BoxConsumer] Received message:{message.body}"
                    )
                    async with message.process():
                        data = json.loads(message.body)
                        dto = BoxDTO(**data)
                        box = map_dto_to_entity(dto)
                        await self._register_box_uc(box)
        except Exception as e:
            self._logger.error(
                f"Failed to publish message to RabbitMQ queue "
                f"{self._queue_name}: {e}"
            )