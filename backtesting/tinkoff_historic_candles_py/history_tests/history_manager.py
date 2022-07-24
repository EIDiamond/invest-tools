import logging
from decimal import Decimal

from data_provider.base_data_provider import IDataProvider
from history_tests.strategy_tester import StrategyTester
from history_tests.test_results import TestResults
from trade_system.commissions.base_commission import ICommissionCalculator
from trade_system.signal import SignalType
from trade_system.strategies.base_strategy import IStrategy

__all__ = ("HistoryTestsManager")

logger = logging.getLogger(__name__)


class HistoryTestsManager:
    """
    The manager for testing strategy on historical candles
    """

    def __init__(self, data_provider: IDataProvider, commission_calculator: ICommissionCalculator) -> None:
        self.__data_provider = data_provider
        self.__commission_calculator = commission_calculator

    def start(
            self,
            strategy: IStrategy,
            from_days: int = 7
    ) -> None:
        """
        Main entry point to start testing
        """
        logger.info(f"Start strategy tests: {strategy}")

        try:
            test_results = StrategyTester(strategy).test(
                self.__data_provider,
                from_days
            )

            # Show all results to log file
            self.__log_test_results(test_results)
        except Exception as ex:
            logger.error(f"Testing error: {repr(ex)}")
        else:
            logger.info("End strategy tests")

    def __log_test_results(self, test_results: TestResults) -> None:
        """
        Just print results to log file
        """
        logger.info("Test Results:")

        logger.info(f"Current Signal: {test_results.current_position}")
        logger.info(f"Signals executed: {len(test_results.executed_orders)}")
        logger.info(f"Take Profit: {len(test_results.get_take_profit_positions())}")
        logger.info(f"Stop Loss: {len(test_results.get_stop_loss_positions())}")

        profit = Decimal(0)
        total_commission = Decimal(0)

        for test_order in test_results.executed_orders:
            logger.info(f"Executed order. {test_order.signal}.")
            logger.info(f"Order profit result: {test_order.is_take_profit()}.")
            logger.info(f"Open: {test_order.open_level}; Close: {test_order.close_level}")

            commission = self.__commission_calculator.calculate(test_order.open_level) + \
                         self.__commission_calculator.calculate(test_order.open_level)
            total_commission += commission
            logger.info(f"Commission: {commission}")

            if test_order.signal.signal_type == SignalType.LONG:
                # long profit if close > open
                profit = profit + test_order.close_level - test_order.open_level
            else:
                # short profit if open > close
                profit = profit + test_order.open_level - test_order.close_level

        logger.info(f"Trade order profit: {profit}")
        logger.info(f"Total commission: {total_commission}")
        logger.info(f"Trade summary: {profit - total_commission}")
