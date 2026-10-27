import sqlite3
import os
import json
import time
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apex_terminal.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite tables for persistent financial data and analysis records."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Ticker Quotes & Overview
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticker_overview (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            sector TEXT,
            industry TEXT,
            current_price REAL,
            previous_close REAL,
            day_high REAL,
            day_low REAL,
            fifty_two_week_high REAL,
            fifty_two_week_low REAL,
            change REAL,
            change_pct REAL,
            market_cap INTEGER,
            pe_ratio REAL,
            forward_pe REAL,
            peg_ratio REAL,
            beta REAL,
            dividend_yield REAL,
            target_mean_price REAL,
            recommendation_key TEXT,
            updated_at REAL
        )
    """)

    # 2. Daily OHLCV Bars (Persistent Historical Data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ohlcv_bars (
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (symbol, date)
        )
    """)

    # 3. AI Analysis Reports History (Track past decisions & score drift)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            composite_score REAL,
            recommendation TEXT,
            target_price REAL,
            expected_return REAL,
            rsi REAL,
            intrinsic_value REAL,
            executive_summary TEXT,
            full_payload_json TEXT,
            created_at REAL
        )
    """)

    # 4. User Watchlist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            symbol TEXT PRIMARY KEY,
            added_at REAL
        )
    """)

    conn.commit()
    conn.close()

# Save/Load Ticker Bundle
def save_bundle_to_db(bundle: Dict[str, Any]):
    """Store or update ticker overview and OHLCV chart bars in SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    now = time.time()
    
    o = bundle["overview"]
    cursor.execute("""
        INSERT INTO ticker_overview (
            symbol, name, sector, industry, current_price, previous_close,
            day_high, day_low, fifty_two_week_high, fifty_two_week_low,
            change, change_pct, market_cap, pe_ratio, forward_pe,
            peg_ratio, beta, dividend_yield, target_mean_price,
            recommendation_key, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(symbol) DO UPDATE SET
            name=excluded.name, sector=excluded.sector, industry=excluded.industry,
            current_price=excluded.current_price, previous_close=excluded.previous_close,
            day_high=excluded.day_high, day_low=excluded.day_low,
            fifty_two_week_high=excluded.fifty_two_week_high,
            fifty_two_week_low=excluded.fifty_two_week_low,
            change=excluded.change, change_pct=excluded.change_pct,
            market_cap=excluded.market_cap, pe_ratio=excluded.pe_ratio,
            forward_pe=excluded.forward_pe, peg_ratio=excluded.peg_ratio,
            beta=excluded.beta, dividend_yield=excluded.dividend_yield,
            target_mean_price=excluded.target_mean_price,
            recommendation_key=excluded.recommendation_key,
            updated_at=excluded.updated_at
    """, (
        o["symbol"], o["name"], o["sector"], o["industry"], o["currentPrice"], o["previousClose"],
        o["dayHigh"], o["dayLow"], o["fiftyTwoWeekHigh"], o["fiftyTwoWeekLow"],
        o["change"], o["changePct"], o["marketCap"], o["peRatio"], o["forwardPE"],
        o["pegRatio"], o["beta"], o["dividendYield"], o["targetMeanPrice"],
        o["recommendationKey"], now
    ))

    # Bulk insert/replace OHLCV bars
    bars = bundle.get("chartBars", [])
    bar_rows = [
        (o["symbol"], b["time"], b["open"], b["high"], b["low"], b["close"], b["volume"])
        for b in bars
    ]
    cursor.executemany("""
        INSERT INTO ohlcv_bars (symbol, date, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(symbol, date) DO UPDATE SET
            open=excluded.open, high=excluded.high, low=excluded.low,
            close=excluded.close, volume=excluded.volume
    """, bar_rows)

    conn.commit()
    conn.close()

def get_bundle_from_db(symbol: str, max_age_seconds: int = 300) -> Optional[Dict[str, Any]]:
    """Retrieve bundle from SQLite if fresh within max_age_seconds (default 5 min)."""
    clean_sym = symbol.upper().strip()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ticker_overview WHERE symbol = ?", (clean_sym,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    age = time.time() - row["updated_at"]
    if age > max_age_seconds:
        conn.close()
        return None # Stale, needs refresh

    # Fetch bars
    cursor.execute("""
        SELECT date, open, high, low, close, volume
        FROM ohlcv_bars
        WHERE symbol = ?
        ORDER BY date ASC
    """, (clean_sym,))
    bar_rows = cursor.fetchall()
    conn.close()

    if len(bar_rows) < 10:
        return None

    chart_bars = [
        {
            "time": r["date"],
            "open": r["open"],
            "high": r["high"],
            "low": r["low"],
            "close": r["close"],
            "volume": r["volume"]
        }
        for r in bar_rows
    ]

    overview = {
        "symbol": row["symbol"],
        "name": row["name"],
        "sector": row["sector"],
        "industry": row["industry"],
        "currentPrice": row["current_price"],
        "previousClose": row["previous_close"],
        "dayHigh": row["day_high"],
        "dayLow": row["day_low"],
        "fiftyTwoWeekHigh": row["fifty_two_week_high"],
        "fiftyTwoWeekLow": row["fifty_two_week_low"],
        "change": row["change"],
        "changePct": row["change_pct"],
        "marketCap": row["market_cap"],
        "peRatio": row["pe_ratio"],
        "forwardPE": row["forward_pe"],
        "pegRatio": row["peg_ratio"],
        "beta": row["beta"],
        "dividendYield": row["dividend_yield"],
        "targetMeanPrice": row["target_mean_price"],
        "recommendationKey": row["recommendation_key"],
        "isDbCached": True,
        "cacheAgeSeconds": round(age, 1)
    }

    return {
        "overview": overview,
        "chartBars": chart_bars
    }

# Analysis History Log
def save_analysis_to_db(symbol: str, full_payload: Dict[str, Any]):
    """Log an AI committee analysis run into SQLite history."""
    clean_sym = symbol.upper().strip()
    conn = get_connection()
    cursor = conn.cursor()

    cio = full_payload.get("committee", {}).get("cio", {})
    fund = full_payload.get("committee", {}).get("fundamental", {})
    tech = full_payload.get("technicalIndicators", {})

    cursor.execute("""
        INSERT INTO analysis_history (
            symbol, composite_score, recommendation, target_price,
            expected_return, rsi, intrinsic_value, executive_summary,
            full_payload_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        clean_sym,
        cio.get("compositeScore", 50.0),
        cio.get("recommendation", "HOLD"),
        cio.get("targetPrice", 0.0),
        cio.get("expectedReturn", 0.0),
        tech.get("rsi", 50.0),
        fund.get("intrinsicValue", 0.0),
        cio.get("executiveSummary", ""),
        json.dumps(full_payload),
        time.time()
    ))

    conn.commit()
    conn.close()

def get_recent_analysis_history(symbol: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve recent AI analysis logs."""
    conn = get_connection()
    cursor = conn.cursor()

    if symbol:
        cursor.execute("""
            SELECT id, symbol, composite_score, recommendation, target_price,
                   expected_return, rsi, intrinsic_value, created_at
            FROM analysis_history
            WHERE symbol = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (symbol.upper().strip(), limit))
    else:
        cursor.execute("""
            SELECT id, symbol, composite_score, recommendation, target_price,
                   expected_return, rsi, intrinsic_value, created_at
            FROM analysis_history
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "symbol": r["symbol"],
            "score": r["composite_score"],
            "recommendation": r["recommendation"],
            "targetPrice": r["target_price"],
            "expectedReturn": r["expected_return"],
            "rsi": r["rsi"],
            "intrinsicValue": r["intrinsic_value"],
            "createdAt": r["created_at"],
            "timeFormatted": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r["created_at"]))
        }
        for r in rows
    ]

# Watchlist Management
def toggle_watchlist_symbol(symbol: str) -> bool:
    """Add or remove a symbol from watchlist. Returns True if now in watchlist."""
    clean_sym = symbol.upper().strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM watchlist WHERE symbol = ?", (clean_sym,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM watchlist WHERE symbol = ?", (clean_sym,))
        in_watchlist = False
    else:
        cursor.execute("INSERT INTO watchlist (symbol, added_at) VALUES (?, ?)", (clean_sym, time.time()))
        in_watchlist = True
    conn.commit()
    conn.close()
    return in_watchlist

def get_watchlist_symbols() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM watchlist ORDER BY added_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [r["symbol"] for r in rows]

# Auto-initialize DB on import
init_db()
