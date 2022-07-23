from decimal import Decimal

from trade_system.signal import TestPosition, Signal

__all__ = ("TestResults")


class TestResults:
    def __init__(self) -> None:
        self.__current_position: TestPosition = None
        self.__executed_orders: list[TestPosition] = []

    @property
    def current_position(self) -> TestPosition:
        return self.__current_position

    @property
    def executed_orders(self) -> list[TestPosition]:
        return self.__executed_orders

    def open_position(self, signal: Signal, open_level: Decimal) -> None:
        if self.__current_position:
            raise Exception("Cannot open position. Current position is exist.")
        else:
            self.__current_position = TestPosition(signal, open_level)

    def close_position_take_profit(self, close_level: Decimal) -> None:
        if self.__current_position:
            self.__current_position.take_profit_executed(close_level)

            self.__execute_current_position()
        else:
            raise Exception("Cannot close position. Current position isn't exist.")

    def close_position_stop_loss(self, close_level: Decimal) -> None:
        if self.__current_position:
            self.__current_position.stop_loss_executed(close_level)

            self.__execute_current_position()
        else:
            raise Exception("Cannot close position. Current position isn't exist.")

    def get_take_profit_positions(self) -> list[TestPosition]:
        return list(filter(lambda x: x.is_take_profit(), self.__executed_orders))

    def get_stop_loss_positions(self) -> list[TestPosition]:
        return list(filter(lambda x: x.is_stop_loss(), self.__executed_orders))

    def get_opened_positions(self) -> list[TestPosition]:
        return list(filter(lambda x: x.is_opened(), self.__executed_orders))

    def __execute_current_position(self) -> None:
        self.__executed_orders.append(self.__current_position)
        self.__current_position = None
