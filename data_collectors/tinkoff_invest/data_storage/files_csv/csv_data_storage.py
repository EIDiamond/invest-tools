import logging

from tinkoff.invest import MarketDataResponse

from configuration.settings import StorageSettings
from data_storage.base_storage import IStorage


__all__ = ("CVSDataStorage")

logger = logging.getLogger(__name__)


class CSVDataStorage(IStorage):
    # Consts to read and parse dict with configuration
    __ROOT_PATH_NAME = "root_path"
    __BUFFER_ROW_SIZE_NAME = "buffer_row_size"

    def __init__(self, settings: StorageSettings) -> None:
        self.__root_path = settings.settings.get(self.__ROOT_PATH_NAME, None)

        self.__buffer_row_size = settings.settings.get(self.__BUFFER_ROW_SIZE_NAME, None)

        if not (self.__root_path and self.__buffer_row_size):
            logger.error(f"Storage init failed: root path is {self.__root_path}, "
                         f"buffer row size is {self.__buffer_row_size}")
            raise Exception(f"CSVDataStorage: All settings must be specified, but some of them is empty")

    def save(self, market_data: MarketDataResponse) -> None:
        pass
