import datetime
import logging
import os
import time

from logging.handlers import RotatingFileHandler

from configuration.configuration import ProgramConfiguration
from data_storage.storage_factory import StorageFactory
from invest_api.services.instrument_service import InstrumentService
from invest_api.services.market_data_stream_service import MarketDataStreamService

# the configuration file name
CONFIG_FILE = "settings.ini"

logger = logging.getLogger(__name__)


def prepare_logs():
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        handlers=[RotatingFileHandler('logs/collector.log', maxBytes=100000000, backupCount=10, encoding='utf-8')],
        encoding="utf-8"
    )


def sleep_to(next_time: datetime) -> None:
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

    logger.debug(f"Sleep from {now} to {next_time}")
    total_seconds = (next_time - now).total_seconds()

    if total_seconds > 0:
        time.sleep(total_seconds)


if __name__ == '__main__':
    prepare_logs()

    logger.info("Data collector has been started")

    try:
        config = ProgramConfiguration(CONFIG_FILE)
        logger.info("Configuration has been loaded")

        logger.info("Load data storage by configuration")
        data_storage = StorageFactory.new_factory(config.storage_type_name, config.storage_settings)

        if data_storage:
            is_trading_day, start_time, end_time = InstrumentService(
                config.tinkoff_token,
                config.tinkoff_app_name
            ).moex_today_trading_schedule()

            if is_trading_day and datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) <= end_time:
                logger.info(f"Today is trading day. Trading will start after {start_time}")

                sleep_to(start_time)

                logger.info(f"Trading day has been started")

                for marketdata in MarketDataStreamService(
                        config.tinkoff_token,
                        config.tinkoff_app_name
                ).market_data_stream(
                    config.download_figi,
                    config.data_collection_settings
                ):
                    data_storage.save(marketdata)

            else:
                logger.info("Nothing collect today")

                if is_trading_day:
                    logger.info("Trade session was over")
                else:
                    logger.info("Today is not trading day")
        else:
            logger.info(f"Storage hasn't been found by type name: {config.storage_type_name}")

    except Exception as ex:
        logger.error(f"Error has been occurred: {repr(ex)}")

    logger.info("Data collector has been finished.")
