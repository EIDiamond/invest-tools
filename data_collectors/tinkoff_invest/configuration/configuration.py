from configparser import ConfigParser

__all__ = ("ProgramConfiguration")

from configuration.settings import DataCollectionSettings, StockFigi


class ProgramConfiguration:
    """
    Represent collector configuration
    """

    def __init__(self, file_name: str) -> None:
        # classic ini file
        config = ConfigParser()
        config.read(file_name)

        self.__tinkoff_token = config["INVEST_API"]["TOKEN"]
        self.__tinkoff_app_name = config["INVEST_API"]["APP_NAME"]

        self.__data_collection_settings = DataCollectionSettings(
            candles=bool(int(config["DATA_COLLECTION"]["CANDLES"])),
            trades=bool(int(config["DATA_COLLECTION"]["TRADES"])),
            order_book=bool(int(config["DATA_COLLECTION"]["ORDER_BOOK"])),
            info=bool(int(config["DATA_COLLECTION"]["INFO"])),
            last_price=bool(int(config["DATA_COLLECTION"]["LAST_PRICE"]))
        )

        self.__stock_figies: list[StockFigi] = []
        for ticker_key, figi_value in config["STOCK_FIGI"].items():
            self.__stock_figies.append(
                StockFigi(
                    ticker=ticker_key,
                    figi=figi_value
                )
            )

    @property
    def tinkoff_token(self) -> str:
        return self.__tinkoff_token

    @property
    def tinkoff_app_name(self) -> str:
        return self.__tinkoff_app_name

    @property
    def data_collection_settings(self) -> DataCollectionSettings:
        return self.__data_collection_settings

    @property
    def download_figi(self) -> list[str]:
        return [stock.figi for stock in self.__stock_figies]
