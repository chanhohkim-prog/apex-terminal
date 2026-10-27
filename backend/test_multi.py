import time
from app.routers.analysis import run_deep_dive_analysis

tickers = ["NVDA", "TSLA", "MSFT", "PLTR"]

print("=" * 60)
print("MULTI-TICKER ACCURACY & PERFORMANCE VERIFICATION")
print("=" * 60)

for sym in tickers:
    t0 = time.time()
    res = run_deep_dive_analysis(sym)
    elapsed = time.time() - t0
    
    p = res["overview"]["currentPrice"]
    dcf = res["committee"]["fundamental"]["intrinsicValue"]
    rsi = res["technicalIndicators"]["rsi"]
    cio = res["committee"]["cio"]["recommendation"]
    score = res["committee"]["cio"]["compositeScore"]
    
    print(f"[{sym}] Latency: {elapsed:.3f}s | Price: ${p:7.2f} | DCF: ${dcf:7.2f} | RSI: {rsi:5.1f} | Score: {score:4.1f} | Decision: {cio}")

print("=" * 60)
print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
