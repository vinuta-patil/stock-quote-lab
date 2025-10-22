# Stock Quote Lab

This project is a simple Python program that retrieves real-time stock information using the **Yahoo Finance API** via the `yfinance` library.  
It was created as part of a networking programming lab assignment to practice Python’s API and networking capabilities.

---

## 🧠 Features
- Prompts the user to enter a stock symbol (e.g., AAPL, MSFT, GOOGL, ADBE)
- Displays:
  - Current local date and time
  - Full company name
  - Current stock price
  - Absolute and percentage value changes
- Handles errors gracefully (e.g., invalid symbol, no network, missing data)
- Runs in a loop until the user types `q` to quit

---

## ⚙️ Requirements
- Python 3.7 or higher
- [`yfinance`](https://pypi.org/project/yfinance/) library

Install the required package:
```bash
pip install yfinance

