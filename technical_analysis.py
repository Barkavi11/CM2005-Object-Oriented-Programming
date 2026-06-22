from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import csv
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class MarketCandle:
    date: str
    pair: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float


@dataclass(frozen=True)
class UserTrade:
    timestamp: str
    pair: str
    side: str
    quantity: float
    price: float


MARKET_HEADERS = ["date", "pair", "open", "high", "low", "close", "volume"]
USER_HEADERS = ["timestamp", "pair", "side", "quantity", "price"]


def _float(value: str, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value for {field_name}: {value}") from exc


def load_market_data(market_csv_path: str | Path) -> List[MarketCandle]:
    records: List[MarketCandle] = []
    with Path(market_csv_path).open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != MARKET_HEADERS:
            raise ValueError("Market data CSV does not match required headers")

        for row in reader:
            records.append(
                MarketCandle(
                    date=row["date"],
                    pair=row["pair"],
                    open_price=_float(row["open"], "open"),
                    high_price=_float(row["high"], "high"),
                    low_price=_float(row["low"], "low"),
                    close_price=_float(row["close"], "close"),
                    volume=_float(row["volume"], "volume"),
                )
            )
    return records


def extract_close_prices(candles: Iterable[MarketCandle], pair: str) -> List[float]:
    return [candle.close_price for candle in candles if candle.pair.upper() == pair.upper()]


def calculate_sma(prices: List[float], period: int) -> float:
    if period <= 0:
        raise ValueError("Period must be a positive integer")
    if len(prices) < period:
        raise ValueError("Not enough prices for SMA calculation")
    subset = prices[-period:]
    return sum(subset) / period


def calculate_ema(prices: List[float], period: int) -> float:
    if period <= 0:
        raise ValueError("Period must be a positive integer")
    if len(prices) < period:
        raise ValueError("Not enough prices for EMA calculation")

    smoothing = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for price in prices[period:]:
        ema = (price - ema) * smoothing + ema
    return ema


def ensure_user_file(user_csv_path: str | Path) -> None:
    user_path = Path(user_csv_path)
    if not user_path.exists():
        user_path.parent.mkdir(parents=True, exist_ok=True)
        with user_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(USER_HEADERS)


def append_user_trade(
    user_csv_path: str | Path,
    pair: str,
    side: str,
    quantity: float,
    price: float,
    timestamp: str | None = None,
) -> None:
    normalized_side = side.upper()
    if normalized_side not in {"BUY", "SELL"}:
        raise ValueError("Side must be BUY or SELL")
    if quantity <= 0 or price <= 0:
        raise ValueError("Quantity and price must be positive")

    ensure_user_file(user_csv_path)
    trade_time = timestamp or datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    with Path(user_csv_path).open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([trade_time, pair.upper(), normalized_side, quantity, price])


def load_user_trades(user_csv_path: str | Path) -> List[UserTrade]:
    ensure_user_file(user_csv_path)
    trades: List[UserTrade] = []

    with Path(user_csv_path).open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != USER_HEADERS:
            raise ValueError("User data CSV does not match required headers")

        for row in reader:
            trades.append(
                UserTrade(
                    timestamp=row["timestamp"],
                    pair=row["pair"],
                    side=row["side"],
                    quantity=_float(row["quantity"], "quantity"),
                    price=_float(row["price"], "price"),
                )
            )

    return trades


def calculate_position_summary(trades: Iterable[UserTrade], pair: str) -> dict[str, float]:
    normalized_pair = pair.upper()
    filtered = [trade for trade in trades if trade.pair.upper() == normalized_pair]

    buy_qty = sum(t.quantity for t in filtered if t.side.upper() == "BUY")
    sell_qty = sum(t.quantity for t in filtered if t.side.upper() == "SELL")
    net_qty = buy_qty - sell_qty

    buy_notional = sum(t.quantity * t.price for t in filtered if t.side.upper() == "BUY")
    avg_buy_price = buy_notional / buy_qty if buy_qty else 0.0

    return {
        "buy_quantity": buy_qty,
        "sell_quantity": sell_qty,
        "net_quantity": net_qty,
        "average_buy_price": avg_buy_price,
    }
