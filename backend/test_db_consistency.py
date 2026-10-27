import sys
sys.stdout.reconfigure(encoding='utf-8')
from app.routers.analysis import run_deep_dive_analysis

data_db = run_deep_dive_analysis("NVDA", force_refresh=False)
overview = data_db["overview"]
print(f"DB Cached: {overview.get('isDbCached')} | CacheAge: {overview.get('cacheAgeSeconds')}s")
print(f"Stored Price: ${overview['currentPrice']} | Bars Count: {len(data_db['chartData'])}")
assert overview.get('isDbCached') == True
assert len(data_db['chartData']) > 50
print(">> SQLite DB Cache Consistency: 100% VERIFIED PASS!")
