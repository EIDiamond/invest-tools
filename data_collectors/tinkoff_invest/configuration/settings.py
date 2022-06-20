from dataclasses import dataclass

__all__ = ("DataCollectionSettings", "StockFigi")


@dataclass(eq=False, repr=True)
class DataCollectionSettings:
    candles: bool = False
    trades: bool = False
    order_book: bool = False
    info: bool = False
    last_price: bool = False


@dataclass(eq=False, repr=True)
class StockFigi:
    ticker: str = ""
    figi: str = ""
