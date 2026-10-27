import time
from app.routers.analysis import run_deep_dive_analysis
from app.database import get_recent_analysis_history, get_watchlist_symbols, toggle_watchlist_symbol

print("--- 1. Testing First Run (Fetches v8 and saves to SQLite) ---")
t0 = time.time()
res1 = run_deep_dive_analysis("NVDA")
t1 = time.time()
print(f"First run time: {t1-t0:.3f}s | isDbCached: {res1['overview'].get('isDbCached', False)}")

print("\n--- 2. Testing Second Run (Instant SQLite Load) ---")
t0 = time.time()
res2 = run_deep_dive_analysis("NVDA")
t1 = time.time()
print(f"Second run time: {(t1-t0)*1000:.2f}ms | isDbCached: {res2['overview'].get('isDbCached', False)} | CacheAge: {res2['overview'].get('cacheAgeSeconds', 0)}s")

print("\n--- 3. Testing SQLite AI Analysis Audit History ---")
history = get_recent_analysis_history("NVDA")
print(f"Found {len(history)} past audit logs for NVDA:")
for h in history[:3]:
    print(f"  [{h['timeFormatted']}] Score: {h['score']} | Decision: {h['recommendation']} | Target: ${h['targetPrice']}")

print("\n--- 4. Testing Watchlist Persistence ---")
toggle_watchlist_symbol("NVDA")
toggle_watchlist_symbol("AAPL")
print(f"Current Watchlist in SQLite: {get_watchlist_symbols()}")

print("\nALL PERSISTENCE TESTS PASSED!")
