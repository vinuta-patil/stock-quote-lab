#!/usr/bin/env python3
"""
Stock Quote CLI (yfinance-based)
- Fetches company name, price, absolute & percent change
- Handles invalid symbols, missing data, and network errors
- Loops so you can query multiple tickers
- Requires: pip install yfinance
"""

import sys
import time
from datetime import datetime
from typing import Optional

try:
    import yfinance as yf
except Exception as e:
    print("This script requires the 'yfinance' package.\n"
          "Install it with: pip install yfinance\n")
    raise

def now_str() -> str:
    return datetime.now().astimezone().strftime("%a %b %d %H:%M:%S %Z %Y")


class QuoteError(Exception):
    pass


def fetch_quote(symbol: str) -> dict:
    """
    Returns a dict with keys: name, symbol, price, change, change_percent, currency
    Raises QuoteError on invalid ticker or missing data.
    """
    t = yf.Ticker(symbol)
    try:
        fi = t.fast_info  # lightweight (price, previous close, currency, etc.)
    except Exception as e:
        raise QuoteError(f"Failed to fetch fast info: {e}")

    price = getattr(fi, "last_price", None)
    prev = getattr(fi, "previous_close", None)
    currency = getattr(fi, "currency", "") or ""

    if price is None or prev is None:
        raise QuoteError("Missing price/previous close (invalid symbol or data unavailable)")

    change = float(price) - float(prev)
    change_percent = (change / float(prev) * 100.0) if prev else 0.0

    # Try to get a proper company name; fall back gracefully
    name: Optional[str] = None
    try:
        info = t.get_info()  # may be slower; wrapped in try
        name = info.get("longName") or info.get("shortName")
    except Exception:
        name = None

    return {
        "name": name or symbol.upper(),
        "symbol": symbol.upper(),
        "price": float(price),
        "change": float(change),
        "change_percent": float(change_percent),
        "currency": currency,
    }


def format_quote(q: dict) -> str:
    sign = "+" if q["change"] >= 0 else ""
    return (
        f"{now_str()}\n\n"
        f"{q['name']} ({q['symbol']})\n\n"
        f"{q['price']:.2f} {sign}{q['change']:.2f} ({sign}{q['change_percent']:.2f}%)"
        + (f" {q['currency']}" if q['currency'] else "")
    )


def main():
    print("Stock Quote (yfinance)")
    print("Example tickers: AAPL, MSFT, GOOGL, ADBE")
    print("Type 'q' to quit.\n")
    while True:
        try:
            symbol = input("Please enter a symbol: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not symbol:
            print("  (!) Please enter a non-empty symbol.\n")
            continue
        if symbol.lower() in {"q", "quit", "exit"}:
            print("Goodbye!")
            return

        try:
            q = fetch_quote(symbol)
            print("\n" + format_quote(q) + "\n")
        except QuoteError as e:
            print(f"\nError: {e}\n")
        except Exception as e:
            print(f"\nUnexpected error: {e}\n")

        time.sleep(0.2)


if __name__ == "__main__":
    main()
