import csv
import yfinance as yf

SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "JPM"]

rows = []
for symbol in SYMBOLS:
    ticker = yf.Ticker(symbol)
    info = ticker.fast_info
    price = info["last_price"]
    prev_close = info["previous_close"]
    change = price - prev_close
    change_pct = (change / prev_close) * 100
    name = ticker.info.get("shortName", symbol)
    rows.append({
        "symbol": symbol,
        "name": name,
        "price": round(price, 2),
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
    })
    print(f"{symbol}: {name} price={price:.2f} change={change:.2f} ({change_pct:.2f}%)")

with open("stock_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["symbol", "name", "price", "change", "change_pct"])
    writer.writeheader()
    writer.writerows(rows)

print("Saved stock_data.csv")
