import enum
from decimal import Decimal

from trade_system.signal import Signal

__all__ = ("TestResults", "TestPosition", "PositionStatus")


@enum.unique
class PositionStatus(enum.IntEnum):
    OPEN = 0
    PROFIT = 1
    LOSS = 2


class TestPosition:
    def __init__(self, signal: Signal, open_level: Decimal) -> None:
        self.__signal = signal
        self.__status = PositionStatus.OPEN
        self.__open_level = open_level
        self.__close_level = Decimal(0)

    @property
    def signal(self) -> Signal:
        return self.__signal

    @property
    def open_level(self) -> Decimal:
        return self.__open_level

    @property
    def close_level(self) -> Decimal:
        return self.__close_level

    def stop_loss_executed(self, close_level: Decimal) -> None:
        self.__status = PositionStatus.LOSS
        self.__close_level = close_level

    def take_profit_executed(self, close_level: Decimal) -> None:
        self.__status = PositionStatus.PROFIT
        self.__close_level = close_level

    def is_opened(self) -> bool:
        return self.__status == PositionStatus.OPEN

    def is_take_profit(self) -> bool:
        return self.__status == PositionStatus.PROFIT

    def is_stop_loss(self) -> bool:
        return self.__status == PositionStatus.LOSS


class TestResults:
    """Class keeps information about trading result (emulation):
    - Current open position
    - All positions for history
    - Signal for position
    - Open and close price level
    """

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

    def __execute_current_position(self) -> None:
        self.__executed_orders.append(self.__current_position)
        self.__current_position = None


