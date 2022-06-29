import datetime
import logging
import time

from configuration.settings import DataCollectionSettings
from data_storage.base_storage import IStorage
from invest_api.services.instrument_service import InstrumentService
from invest_api.services.market_data_stream_service import MarketDataStreamService

__all__ = ("TinkoffCollector")

logger = logging.getLogger(__name__)


class TinkoffCollector:
    """
    The class encapsulate market data collection process
    """
    def __init__(
            self,
            token: str,
            app_name: str,
            storage: IStorage
    ) -> None:
        self.__token = token
        self.__app_name = app_name

        self.__storage = storage

    def collect(
            self,
            download_figi: list[str],
            data_collection_settings: DataCollectionSettings
    ) -> None:
        is_trading_day, start_time, end_time = InstrumentService(
            self.__token,
            self.__app_name
        ).moex_today_trading_schedule()

        if is_trading_day and datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) <= end_time:
            logger.info(f"Today is trading day. Trading will start after {start_time}")

            TinkoffCollector.__sleep_to(start_time)

            logger.info(f"Trading day has been started")

            for marketdata in MarketDataStreamService(
                    self.__token,
                    self.__app_name
            ).market_data_stream(
                download_figi,
                data_collection_settings
            ):
                self.__storage.save(marketdata)

        else:
            logger.info("Nothing collect today")

            if is_trading_day:
                logger.info("Trade session was over")
            else:
                logger.info("Today is not trading day")

    @staticmethod
    def __sleep_to(next_time: datetime) -> None:
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

        logger.debug(f"Sleep from {now} to {next_time}")
        total_seconds = (next_time - now).total_seconds()

        if total_seconds > 0:
            time.sleep(total_seconds)
