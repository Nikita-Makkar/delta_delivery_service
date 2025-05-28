from delivery_service.application.interfaces.cache import ICache
from delivery_service.application.interfaces.exchange_rate import IExchangeRate
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.box_repository import \
    IBoxRepository
from delivery_service.application.use_cases.register_box import \
    RegisterBoxUseCase
from delivery_service.domain.interfaces.delivery_price_calculator import \
    IDeliveryPriceCalculator
from delivery_service.domain.services.default_price_calculator import \
    DefaultPriceCalculator
from delivery_service.infrastructure.logger.factory import LoggerFactory
from delivery_service.infrastructure.rabbitmq.consumer import BoxConsumer
from delivery_service.infrastructure.services.cbr_exchange_rate import \
    CbrExchangeRate
from delivery_service.infrastructure.services.redis_cache import RedisCache
from delivery_service.infrastructure.sqlalchemy.repositories.box import \
    BoxRepository
from delivery_service.infrastructure.sqlalchemy.unit_of_work import \
    SQLAlchemyUnitOfWork


def get_logger() -> ILogger:
    return LoggerFactory().get_logger()


def get_register_box_uc(logger: ILogger) -> RegisterBoxUseCase:
    """
    Builds RegisterBoxUseCase with all dependencies.
    """
    uow: IUnitOfWork = SQLAlchemyUnitOfWork()
    repository: type[IBoxRepository] = BoxRepository
    cache_service: ICache = RedisCache(logger)
    rate_provider: IExchangeRate = CbrExchangeRate(cache_service, logger)
    price_calculator: IDeliveryPriceCalculator = DefaultPriceCalculator()

    return RegisterBoxUseCase(
        uow,
        repository,
        rate_provider,
        price_calculator,
        logger,
    )


async def start_consumer() -> None:
    """
    Starts RabbitMQ consumer for box registration.
    """
    logger = get_logger()
    consumer = BoxConsumer(
        register_box_uc=get_register_box_uc(logger), logger=logger
    )
    await consumer.start()
