import time
import requests

def test_v8_fetch(symbol: str):
    t0 = time.time()
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1y&interval=1d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=5)
    data = r.json()
    meta = data["chart"]["result"][0]["meta"]
    t1 = time.time()
    print(f"Direct v8 fetch time: {t1-t0:.3f}s")
    print(f"Symbol: {meta.get('symbol')}, Price: {meta.get('regularMarketPrice')}, PrevClose: {meta.get('chartPreviousClose')}")
    print(f"52W High: {meta.get('fiftyTwoWeekHigh')}, 52W Low: {meta.get('fiftyTwoWeekLow')}")

test_v8_fetch("AAPL")
test_v8_fetch("NVDA")
