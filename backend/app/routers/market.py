from fastapi import APIRouter, Query, HTTPException
from app.data_fetcher import get_market_indices, fetch_ticker_bundle, get_ticker_news
from app.database import get_watchlist_symbols, toggle_watchlist_symbol
from typing import Optional

router = APIRouter(prefix="/api/market", tags=["Market Data"])

@router.get("/indices")
def market_indices():
    """Returns top benchmark indices for live ticker tape with parallel caching."""
    return get_market_indices()

@router.get("/overview/{symbol}")
def ticker_overview(symbol: str):
    """Returns high-level statistics and valuation multiples."""
    try:
        bundle = fetch_ticker_bundle(symbol)
        return bundle["overview"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch overview: {str(e)}")

@router.get("/history/{symbol}")
def historical_chart(
    symbol: str,
    period: str = Query("1y", regex="^(1mo|3mo|6mo|1y|2y|5y)$"),
    interval: str = Query("1d", regex="^(1d|1wk|1mo)$")
):
    """Returns OHLCV historical candlestick/line data."""
    try:
        bundle = fetch_ticker_bundle(symbol, range_period=period)
        return bundle["chartBars"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch history: {str(e)}")

@router.get("/news/{symbol}")
def ticker_news(symbol: str):
    """Returns company news headlines."""
    try:
        return get_ticker_news(symbol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch news: {str(e)}")

# Watchlist endpoints
@router.get("/watchlist")
def get_watchlist():
    """Get user's saved watchlist symbols from SQLite."""
    return {"symbols": get_watchlist_symbols()}

@router.post("/watchlist/{symbol}")
def toggle_watchlist(symbol: str):
    """Add or remove ticker from persistent watchlist."""
    is_in_watchlist = toggle_watchlist_symbol(symbol)
    return {
        "symbol": symbol.upper().strip(),
        "inWatchlist": is_in_watchlist,
        "allSymbols": get_watchlist_symbols()
    }
