# CM2005-Object-Oriented-Programming

This repository provides a minimal **technical analysis toolkit** for currency exchange data.

## Features

The CLI (`main.py`) exposes five coursework-oriented tasks:

1. Read market trading CSV data and show close-price summary (read-only market file).
2. Compute simple moving average (SMA) from market close prices.
3. Compute exponential moving average (EMA) from market close prices.
4. Record user trades to a separate user CSV file.
5. Read user trade CSV and show position summary.

Market data is stored in `data/market_trading_data.csv` and is only read by the application.
User data is stored separately in `data/user_trading_data.csv`.

## Run

```bash
python main.py
```

## Test

```bash
python -m unittest discover -s tests -v
```
