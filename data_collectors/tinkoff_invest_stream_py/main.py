import logging
import os

from logging.handlers import RotatingFileHandler

from configuration.configuration import ProgramConfiguration
from data_collector.tinkoff_collector import TinkoffCollector
from data_storage.storage_factory import StorageFactory

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

    try:
        config = ProgramConfiguration(CONFIG_FILE)
        logger.info("Configuration has been loaded")

        logger.info("Load data storage by configuration")
        data_storage = StorageFactory.new_factory(config.storage_type_name, config.storage_settings)

        if data_storage:
            logger.debug("Create data collector")
            market_data_collector = TinkoffCollector(config.tinkoff_token, config.tinkoff_app_name, data_storage)

            market_data_collector.collect(config.download_figi, config.data_collection_settings)

        else:
            logger.info(f"Storage hasn't been found by type name: {config.storage_type_name}")

    except Exception as ex:
        logger.error(f"Error has been occurred: {repr(ex)}")

    logger.info("Data collector has been finished.")
