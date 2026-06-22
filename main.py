from __future__ import annotations

from pathlib import Path

from technical_analysis import (
    append_user_trade,
    calculate_ema,
    calculate_position_summary,
    calculate_sma,
    extract_close_prices,
    load_market_data,
    load_user_trades,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MARKET_FILE = DATA_DIR / "market_trading_data.csv"
USER_FILE = DATA_DIR / "user_trading_data.csv"


def _input_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def _input_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive numeric value.")


def _market_prices(pair: str) -> list[float]:
    candles = load_market_data(MARKET_FILE)
    prices = extract_close_prices(candles, pair)
    if not prices:
        raise ValueError(f"No market data found for pair: {pair.upper()}")
    return prices


def show_menu() -> None:
    print("\n=== Technical Analysis Toolkit ===")
    print("1. View market close-price summary")
    print("2. Calculate simple moving average (SMA)")
    print("3. Calculate exponential moving average (EMA)")
    print("4. Add user trade")
    print("5. View user position summary")
    print("0. Exit")


def handle_choice(choice: int) -> bool:
    if choice == 0:
        print("Goodbye.")
        return False

    if choice == 1:
        pair = input("Currency pair (e.g. EURUSD): ").strip().upper()
        prices = _market_prices(pair)
        print(f"Data points: {len(prices)}")
        print(f"Latest close: {prices[-1]:.5f}")
        return True

    if choice == 2:
        pair = input("Currency pair: ").strip().upper()
        period = _input_int("SMA period: ")
        sma = calculate_sma(_market_prices(pair), period)
        print(f"SMA({period}) for {pair}: {sma:.5f}")
        return True

    if choice == 3:
        pair = input("Currency pair: ").strip().upper()
        period = _input_int("EMA period: ")
        ema = calculate_ema(_market_prices(pair), period)
        print(f"EMA({period}) for {pair}: {ema:.5f}")
        return True

    if choice == 4:
        pair = input("Currency pair: ").strip().upper()
        side = input("Side (BUY/SELL): ").strip().upper()
        quantity = _input_float("Quantity: ")
        price = _input_float("Price: ")
        append_user_trade(USER_FILE, pair=pair, side=side, quantity=quantity, price=price)
        print("Trade saved to user file.")
        return True

    if choice == 5:
        pair = input("Currency pair: ").strip().upper()
        trades = load_user_trades(USER_FILE)
        summary = calculate_position_summary(trades, pair)
        print(f"Buy qty: {summary['buy_quantity']:.4f}")
        print(f"Sell qty: {summary['sell_quantity']:.4f}")
        print(f"Net qty: {summary['net_quantity']:.4f}")
        print(f"Average buy price: {summary['average_buy_price']:.5f}")
        return True

    print("Invalid option. Please choose a value from 0 to 5.")
    return True


def run() -> None:
    while True:
        show_menu()
        choice = _input_int("Select an option: ")
        try:
            if not handle_choice(choice):
                return
        except ValueError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    run()
