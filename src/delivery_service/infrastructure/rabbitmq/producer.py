import json
from dataclasses import asdict

import aio_pika

from delivery_service.application.dto.box import BoxDTO
from delivery_service.application.exceptions import ApplicationError
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.infrastructure.config import settings


class BoxProducer:
    """
    Producer for register box.
    """

    def __init__(
        self,
        logger: ILogger,
        rabbitmq_url: str = settings.RABBITMQ_URL,
        queue_name: str = "register_box",
    ):
        self._rabbitmq_url = rabbitmq_url
        self._queue_name = queue_name
        self._logger = logger

    async def publish(self, box: BoxDTO) -> None:
        """
        Sends box DTO to RabbitMQ queue.
        """
        try:
            self._logger.info(
                f"Connecting to RabbitMQ at {self._rabbitmq_url}"
            )
            connection = await aio_pika.connect_robust(self._rabbitmq_url)
            async with connection:
                channel = await connection.channel()
                await channel.declare_queue(self._queue_name, durable=True)
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(asdict(box)).encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                    ),
                    routing_key=self._queue_name,
                )
                self._logger.info(
                    f"Message published to queue '{self._queue_name}'"
                )
        except Exception as e:
            self._logger.error(
                f"Failed to publish message to RabbitMQ queue '{self._queue_name}': {e}"
            )
            raise ApplicationError("Failed to register box")
