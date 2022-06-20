import logging
import os

from logging.handlers import RotatingFileHandler

from configuration.configuration import ProgramConfiguration
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


if __name__ == '__main__':
    prepare_logs()

    logger.info("Data collector has been started")

    config = ProgramConfiguration(CONFIG_FILE)
    logger.info("Configuration has been loaded")

    for marketdata in MarketDataStreamService(
            config.tinkoff_token,
            config.tinkoff_app_name
    ).market_data_stream(config.download_figi):
        logger.info(marketdata)

    logger.info("Data collector has been finished")
