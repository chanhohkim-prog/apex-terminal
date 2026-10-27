from fastapi import APIRouter, HTTPException, Query
from app.data_fetcher import fetch_ticker_bundle, get_ticker_news
from app.quant_engine import compute_technical_indicators_from_bars, compute_fundamental_metrics_from_overview
from app.agents.fundamental import run_fundamental_agent
from app.agents.technical import run_technical_agent
from app.agents.sentiment import run_sentiment_agent
from app.agents.risk import run_risk_agent
from app.agents.cio import run_cio_agent
from app.database import save_analysis_to_db, get_recent_analysis_history

router = APIRouter(prefix="/api/analysis", tags=["AI Analysis"])

@router.get("/deep-dive/{symbol}")
def run_deep_dive_analysis(
    symbol: str,
    period: str = "1y",
    force_refresh: bool = False
):
    """
    ⚡ ULTRA-FAST PERSISTENT MULTI-AGENT ENGINE:
    1. Checks local SQLite DB (<1ms).
    2. Syncs from live Direct v8 if data is older than 5 minutes or force_refresh=True.
    3. Runs Quant math & 4-Agent Committee.
    4. Automatically commits full audit trail into SQLite history table.
    """
    try:
        clean_symbol = symbol.upper().strip()
        
        # 1. Fetch bundled price & chart bars (Local DB or Direct v8)
        bundle = fetch_ticker_bundle(clean_symbol, range_period=period, force_refresh=force_refresh)
        overview = bundle["overview"]
        chart_bars = bundle["chartBars"]
        news = get_ticker_news(clean_symbol)

        # 2. In-memory Quant calculations
        tech_indicators = compute_technical_indicators_from_bars(chart_bars)
        fund_metrics = compute_fundamental_metrics_from_overview(overview, chart_bars)

        # 3. Multi-Agent Committee execution
        fund_agent = run_fundamental_agent(overview, fund_metrics)
        tech_agent = run_technical_agent(overview, tech_indicators)
        sent_agent = run_sentiment_agent(overview, news)
        risk_agent = run_risk_agent(overview, tech_indicators)

        # 4. Chief Investment Officer synthesis
        cio_verdict = run_cio_agent(overview, fund_agent, tech_agent, sent_agent, risk_agent)

        payload = {
            "symbol": clean_symbol,
            "overview": overview,
            "chartData": chart_bars,
            "news": news,
            "technicalIndicators": tech_indicators,
            "fundamentalMetrics": fund_metrics,
            "committee": {
                "cio": cio_verdict,
                "fundamental": fund_agent,
                "technical": tech_agent,
                "sentiment": sent_agent,
                "risk": risk_agent
            }
        }

        # 5. Persist analysis audit snapshot to SQLite
        try:
            save_analysis_to_db(clean_symbol, payload)
        except Exception as e:
            print(f"Failed to log analysis to DB: {e}")

        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed for {symbol}: {str(e)}")

@router.get("/history/{symbol}")
def get_symbol_analysis_history(symbol: str, limit: int = 10):
    """Retrieve historical AI verdicts and scores for a specific ticker from SQLite."""
    try:
        return get_recent_analysis_history(symbol=symbol, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")

@router.get("/history")
def get_global_analysis_history(limit: int = 20):
    """Retrieve most recent AI analysis runs across all tickers."""
    try:
        return get_recent_analysis_history(symbol=None, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch global history: {str(e)}")
