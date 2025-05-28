from delivery_service.application.exceptions import DatabaseException
from delivery_service.application.interfaces.exchange_rate import IExchangeRate
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.box_repository import \
    IBoxRepository
from delivery_service.domain.entities.box import Box
from delivery_service.domain.interfaces.delivery_price_calculator import \
    IDeliveryPriceCalculator
from delivery_service.domain.value_objects.box_id import BoxId
from delivery_service.domain.value_objects.enums import Currency


class RegisterBoxUseCase:
    """
    Use case for registering a box and calculating its delivery price.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        repository: type[IBoxRepository],
        rate_provider: IExchangeRate,
        price_calculator: IDeliveryPriceCalculator,
        logger: ILogger,
    ):
        self._repository: type[IBoxRepository] = repository
        self._uow: IUnitOfWork = uow
        self._rate_provider: IExchangeRate = rate_provider
        self._price_calculator: IDeliveryPriceCalculator = price_calculator
        self._logger = logger

    async def __call__(self, box: Box) -> BoxId:
        """
        Calculates delivery price and saves box to the database.
        """
        try:
            self._logger.info(
                f"Calculating delivery price for box: {box.id}"
            )
            exchange_rate = await self._rate_provider.get_rate(
                Currency.USD, Currency.RUB
            )
            delivery_price = self._price_calculator.calculate(
                box, exchange_rate
            )
            box.set_delivery_price(delivery_price)
        except Exception as e:
            self._logger.error(
                f"Failed to calculate delivery price box: {e}"
            )

        try:
            async with self._uow as uow:
                repository = self._repository(uow)
                result = await repository.add(box)
                self._logger.info(
                    f"`Box with ID {box.id} successfully registered."
                )
            return result.id
        except DatabaseException as e:
            self._logger.error(f"Failed to register box: {e}")