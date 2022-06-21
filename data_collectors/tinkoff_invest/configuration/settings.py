from dataclasses import dataclass, field

__all__ = ("DataCollectionSettings", "StockFigi", "StorageSettings")


@dataclass(eq=False, repr=True)
class DataCollectionSettings:
    candles: bool = False
    trades: bool = False
    order_book: bool = False
    last_price: bool = False


@dataclass(eq=False, repr=True)
class StockFigi:
    ticker: str = ""
    figi: str = ""


@dataclass(eq=False, repr=True)
class StorageSettings:
    # All internal storage settings are represented as dict. A storage class have to parse it himself.
    # Here, we avoid any strong dependencies and obligations
    settings: dict = field(default_factory=dict)
