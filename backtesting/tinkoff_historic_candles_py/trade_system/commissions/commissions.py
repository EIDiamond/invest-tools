from decimal import Decimal

from configuration.settings import CommissionSettings

__all__ = ("ProgramConfiguration")


class CommissionCalculator:
    def __init__(self, settings: CommissionSettings) -> None:
        self.__settings = settings

    def calculate(self, price: Decimal) -> Decimal:
        return price * self.__settings.every_order
