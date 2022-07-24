import logging

from tinkoff.invest import HistoricCandle
from tinkoff.invest.utils import quotation_to_decimal

from trade_system.strategies.base_strategy import IStrategy
from history_tests.test_results import TestResults

__all__ = ("StrategyTester")

logger = logging.getLogger(__name__)


class StrategyTester:
    """
    Class encapsulate test logic on historical candles
    """
    def __init__(self, strategy: IStrategy) -> None:
        self.__strategy = strategy

    def test(
            self,
            candles: list[HistoricCandle]
    ) -> TestResults:
        logger.info(f"Start test: {self.__strategy}, candles count: {len(candles)}")

        test_result = TestResults()

        for candle in candles:
            # Check price from candle for take or stop price level
            if test_result.current_position:
                high = quotation_to_decimal(candle.high)
                low = quotation_to_decimal(candle.low)

                # Logic is:
                # if stop or take price level is between high and low, then stop or take will be executed
                # candle.close is the nearest price level to emulate price of closed position
                if low <= test_result.current_position.signal.stop_loss_level <= high:
                    logger.info("Test STOP LOSS executed")
                    logger.info(f"CANDLE: {candle}")
                    logger.info(f"Signal: {test_result.current_position.signal}")

                    test_result.close_position_stop_loss(quotation_to_decimal(candle.close))

                elif low <= test_result.current_position.signal.take_profit_level <= high:
                    logger.info("Test TAKE PROFIT executed")
                    logger.info(f"CANDLE: {candle}")
                    logger.info(f"Signal: {test_result.current_position.signal}")

                    test_result.close_position_take_profit(quotation_to_decimal(candle.close))

            signal = self.__strategy.analyze_candle(candle)

            if signal:
                logger.info(f"New Signal: {signal}")

                if test_result.current_position:
                    logger.info("Signal skipped. Old still alive")
                else:
                    # candle.close is the nearest price level to emulate price of open position
                    test_result.open_position(signal, quotation_to_decimal(candle.close))

        logger.info(f"Tests completed")

        return test_result
