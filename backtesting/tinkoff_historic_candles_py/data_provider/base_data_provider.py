import abc
from typing import Generator

from tinkoff.invest import HistoricCandle

__all__ = ("IDataProvider")


class IDataProvider(abc.ABC):
    @abc.abstractmethod
    def provide(self, figi: str, from_days: int) -> Generator[HistoricCandle, None, None]:
        pass
