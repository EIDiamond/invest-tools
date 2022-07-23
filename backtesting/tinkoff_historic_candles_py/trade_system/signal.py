import enum
import logging
from dataclasses import dataclass, field
from decimal import Decimal

__all__ = ("Signal", "SignalType", "TestPosition", "PositionStatus")

logger = logging.getLogger(__name__)


@enum.unique
class SignalType(enum.IntEnum):
    LONG = 0
    SHORT = 1


@dataclass(frozen=True, eq=False, repr=True)
class Signal:
    figi: str = ""
    signal_type: SignalType = SignalType.LONG
    take_profit_level: Decimal = field(default_factory=Decimal)
    stop_loss_level: Decimal = field(default_factory=Decimal)


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
