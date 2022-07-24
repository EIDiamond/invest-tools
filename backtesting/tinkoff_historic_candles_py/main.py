import logging
import os
from logging.handlers import RotatingFileHandler

from configuration.configuration import ProgramConfiguration
from data_provider.tinkoff_historic import TinkoffHistoric
from history_tests.history_manager import HistoryTestsManager
from history_tests.trading_emulator.stop_take_emulator import StopTakeEmulator
from trade_system.commissions.commissions import CommissionEveryOrderCalculator
from trade_system.strategies.strategy_factory import StrategyFactory

# the configuration file name
CONFIG_FILE = "settings.ini"

logger = logging.getLogger(__name__)


def prepare_logs() -> None:
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        handlers=[RotatingFileHandler('logs/test.log', maxBytes=100000000, backupCount=10, encoding='utf-8')],
        encoding="utf-8"
    )


if __name__ == "__main__":
    prepare_logs()

    logger.info("Historical candles backtesting has been started.")

    try:
        config = ProgramConfiguration(CONFIG_FILE)
        logger.info("Configuration has been loaded")
    except Exception as ex:
        logger.critical("Load configuration error: %s", repr(ex))
    else:
        # create data provider
        data_provider = TinkoffHistoric(config.tinkoff_token, config.tinkoff_app_name)
        # create calculator of commissions
        commission_calculator = CommissionEveryOrderCalculator(config.commission_settings)
        # create a strategy for tests
        test_strategy = StrategyFactory.new_factory(
            config.test_strategy_settings.name,
            config.test_strategy_settings
        )
        # create trading emulator
        trading_emulator = StopTakeEmulator(test_strategy)

        # start testing
        HistoryTestsManager(data_provider, commission_calculator).start(trading_emulator)

    logger.info("Backtesting has been ended")
