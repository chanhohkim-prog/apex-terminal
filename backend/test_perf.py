import time
from app.routers.analysis import run_deep_dive_analysis

t0 = time.time()
r = run_deep_dive_analysis('AAPL')
elapsed = time.time() - t0

print(f"Elapsed Time: {elapsed:.2f}s")
print(f"Symbol: {r['symbol']}, Price: {r['overview']['currentPrice']}")
print(f"DCF Fair Value: {r['committee']['fundamental']['intrinsicValue']}")
print(f"RSI: {r['technicalIndicators']['rsi']}")
print(f"CIO Recommendation: {r['committee']['cio']['recommendation']}")
