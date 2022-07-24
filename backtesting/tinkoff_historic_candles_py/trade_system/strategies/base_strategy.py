import abc

from tinkoff.invest import HistoricCandle

from configuration.settings import StrategySettings
from trade_system.signal import Signal

__all__ = ("IStrategy")


class IStrategy(abc.ABC):
    @property
    @abc.abstractmethod
    def settings(self) -> StrategySettings:
        pass

    @abc.abstractmethod
    def analyze_candle(self, candle: HistoricCandle) -> Signal:
        pass
