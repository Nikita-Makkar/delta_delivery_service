import asyncio

from delivery_service.entrypoints.rabbitmq import start_consumer


def run_worker() -> None:
    """
    Starts RabbitMQ consumer worker.
    """

    asyncio.run(start_consumer())


if __name__ == "__main__":
    run_worker()
