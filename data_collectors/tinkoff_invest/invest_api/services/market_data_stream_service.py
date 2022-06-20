import datetime
import logging
from typing import Generator

from tinkoff.invest import Client, CandleInstrument, SubscriptionInterval, InfoInstrument, TradeInstrument, \
    MarketDataResponse, Candle, AsyncClient
from tinkoff.invest.market_data_stream.async_market_data_stream_manager import AsyncMarketDataStreamManager
from tinkoff.invest.market_data_stream.market_data_stream_interface import IMarketDataStreamManager
from tinkoff.invest.market_data_stream.market_data_stream_manager import MarketDataStreamManager

__all__ = ("MarketDataStreamService")

logger = logging.getLogger(__name__)


class MarketDataStreamService:
    """
    The class encapsulate tinkoff market data stream (gRPC) service api
    """
    def __init__(self, token: str, app_name: str) -> None:
        self.__token = token
        self.__app_name = app_name

    def market_data_stream(
            self,
            figies: list[str]
    ) -> Generator[MarketDataResponse, None, None]:
        """
        The method starts gRPC stream and return candles
        """
        logger.debug(f"Starting market data stream")

        with Client(self.__token, app_name=self.__app_name) as client:
            market_data_candles_stream: MarketDataStreamManager = client.create_market_data_stream()

            logger.info(f"Subscribe candles: {figies}")
            market_data_candles_stream.candles.subscribe(
                [
                    CandleInstrument(
                        figi=figi,
                        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE
                    )
                    for figi in figies
                ]
            )

            logger.info(f"Subscribe trades: {figies}")
            market_data_candles_stream.trades.subscribe(
                [
                    TradeInstrument(
                        figi=figi
                    )
                    for figi in figies
                ]
            )

            for market_data in market_data_candles_stream:
                logger.debug(f"market_data: {market_data}")

                if market_data.candle or market_data.trade:
                    yield market_data

    @staticmethod
    def __stop_candles_stream(stream: IMarketDataStreamManager) -> None:
        if stream:
            logger.info(f"Stopping candles stream")
            stream.stop()
