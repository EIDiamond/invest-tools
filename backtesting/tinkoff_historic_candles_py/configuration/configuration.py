from configparser import ConfigParser

from configuration.settings import StrategySettings

__all__ = ("ProgramConfiguration")


class ProgramConfiguration:
    """
    Represent program configuration
    """
    def __init__(self, file_name: str) -> None:
        # classic ini file
        config = ConfigParser()
        config.read(file_name)

        self.__tinkoff_token = config["INVEST_API"]["TOKEN"]
        self.__tinkoff_app_name = config["INVEST_API"]["APP_NAME"]

        self.__test_strategy_settings = \
            StrategySettings(
                name=config["TEST_STRATEGY"]["STRATEGY_NAME"],
                figi=config["TEST_STRATEGY"]["FIGI"],
                ticker=config["TEST_STRATEGY"]["TICKER"],
                max_lots_per_order=int(config["TEST_STRATEGY"]["MAX_LOTS_PER_ORDER"]),
                settings=config["TEST_STRATEGY_SETTINGS"]
            )

    @property
    def tinkoff_token(self) -> str:
        return self.__tinkoff_token

    @property
    def tinkoff_app_name(self) -> str:
        return self.__tinkoff_app_name

    @property
    def test_strategy_settings(self) -> StrategySettings:
        return self.__test_strategy_settings
