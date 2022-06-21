import abc
import logging

from tinkoff.invest import MarketDataResponse


__all__ = ("IStorage")

logger = logging.getLogger(__name__)


class IStorage(abc.ABC):
    @abc.abstractmethod
    def save(self, market_data: MarketDataResponse) -> None:
        pass
