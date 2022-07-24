import abc
from decimal import Decimal

__all__ = ("ICommissionCalculator")


class ICommissionCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate(self, price: Decimal) -> Decimal:
        pass
