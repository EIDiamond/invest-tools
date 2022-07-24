import abc

from data_provider.base_data_provider import IDataProvider
from history_tests.test_results import TestResults

__all__ = ("ITradingEmulator")


class ITradingEmulator(abc.ABC):
    """Interface to emulate different style of trading"""
    @abc.abstractmethod
    def emulate_trading(self, data_provider: IDataProvider, from_days: int) -> TestResults:
        pass
