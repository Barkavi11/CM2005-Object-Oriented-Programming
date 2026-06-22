import csv
import tempfile
import unittest
from pathlib import Path

from technical_analysis import (
    append_user_trade,
    calculate_ema,
    calculate_position_summary,
    calculate_sma,
    ensure_user_file,
    extract_close_prices,
    load_market_data,
    load_user_trades,
)


class TechnicalAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        self.market_csv = self.tmp_path / "market.csv"
        self.user_csv = self.tmp_path / "user.csv"

        with self.market_csv.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["date", "pair", "open", "high", "low", "close", "volume"])
            writer.writerow(["2026-01-01", "EURUSD", "1.1000", "1.1100", "1.0900", "1.1050", "1000"])
            writer.writerow(["2026-01-02", "EURUSD", "1.1050", "1.1200", "1.1000", "1.1150", "1500"])
            writer.writerow(["2026-01-03", "EURUSD", "1.1150", "1.1300", "1.1100", "1.1250", "1600"])

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_load_market_data_and_extract_prices(self) -> None:
        candles = load_market_data(self.market_csv)
        prices = extract_close_prices(candles, "eurusd")
        self.assertEqual(prices, [1.105, 1.115, 1.125])

    def test_sma_and_ema(self) -> None:
        prices = [1.0, 2.0, 3.0, 4.0, 5.0]
        self.assertAlmostEqual(calculate_sma(prices, 3), 4.0)
        self.assertAlmostEqual(calculate_ema(prices, 3), 4.0)

    def test_user_trades_persist_to_separate_file(self) -> None:
        ensure_user_file(self.user_csv)
        append_user_trade(self.user_csv, pair="EURUSD", side="BUY", quantity=2, price=1.2, timestamp="2026-01-01T00:00:00Z")
        append_user_trade(self.user_csv, pair="EURUSD", side="SELL", quantity=0.5, price=1.3, timestamp="2026-01-01T01:00:00Z")

        trades = load_user_trades(self.user_csv)
        summary = calculate_position_summary(trades, "EURUSD")

        self.assertEqual(len(trades), 2)
        self.assertAlmostEqual(summary["buy_quantity"], 2.0)
        self.assertAlmostEqual(summary["sell_quantity"], 0.5)
        self.assertAlmostEqual(summary["net_quantity"], 1.5)


if __name__ == "__main__":
    unittest.main()
