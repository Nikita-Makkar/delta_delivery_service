import httpx

from delivery_service.application.interfaces.cache import ICache
from delivery_service.application.interfaces.exchange_rate import IExchangeRate
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate


class CbrExchangeRate(IExchangeRate):
    """
    Fetches and caches USD to RUB exchange rate from CBR API.
    """

    def __init__(self, cache: ICache, logger: ILogger):
        self._cache = cache
        self._logger = logger

    async def get_rate(
        self, from_currency: Currency, to_currency: Currency
    ) -> ExchangeRate:
        """
        Gets exchange rate, using cache or fetching from CBR API.
        """
        cache_key = "USD_RUB"
        cache_value = await self._cache.get(cache_key)

        if cache_value:
            return ExchangeRate(cache_value, from_currency, to_currency)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.cbr-xml-daily.ru/daily_json.js"
                )
                data = response.json()
                rate = data["Valute"]["USD"]["Value"]
                self._logger.info(f"Fetched exchange rate USD to RUB: {rate}")
        except Exception as e:
            self._logger.error(f"Failed to fetch exchange rate: {e}")
        await self._cache.set(cache_key, rate)
        return ExchangeRate(rate, from_currency, to_currency)
