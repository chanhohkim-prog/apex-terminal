import time
import math
import sys

# Force UTF-8 stdout if needed
sys.stdout.reconfigure(encoding='utf-8')

from app.routers.analysis import run_deep_dive_analysis
from app.database import get_recent_analysis_history, get_watchlist_symbols

def verify_ticker_consistency(symbol: str):
    print(f"\n{'='*70}")
    print(f">> [AUDIT TICKER: {symbol}] Full Consistency & Integrity Check")
    print(f"{'='*70}")

    t0 = time.time()
    data = run_deep_dive_analysis(symbol, force_refresh=True)
    fetch_latency = time.time() - t0

    overview = data["overview"]
    chart_bars = data["chartData"]
    tech = data["technicalIndicators"]
    fund = data["fundamentalMetrics"]
    committee = data["committee"]
    cio = committee["cio"]

    checks = []

    # 1. 시세 및 변동률 수학적 정합성
    cur_price = overview["currentPrice"]
    prev_close = overview["previousClose"]
    calc_change = round(cur_price - prev_close, 2)
    calc_pct = round((calc_change / prev_close) * 100, 2) if prev_close else 0.0

    diff_chg = abs(overview["change"] - calc_change)
    diff_pct = abs(overview["changePct"] - calc_pct)
    price_math_ok = diff_chg < 0.02 and diff_pct < 0.05
    checks.append(("Price & Change Math Integrity", price_math_ok, f"Price=${cur_price}, Prev=${prev_close}, Chg={overview['change']} ({overview['changePct']}%)"))

    # 2. 캔들 차트와 시세 일치 여부
    last_bar = chart_bars[-1] if chart_bars else None
    chart_price_ok = False
    if last_bar:
        chart_price_ok = abs(last_bar["close"] - cur_price) / cur_price < 0.05
        checks.append(("Latest Bar Close vs Current Price", chart_price_ok, f"Latest Bar Close=${last_bar['close']} vs Current=${cur_price}"))
    else:
        checks.append(("Chart Data Presence", False, "No chart bars returned"))

    # 3. 52주 최고/최저 범위 유효성
    h52 = overview["fiftyTwoWeekHigh"]
    l52 = overview["fiftyTwoWeekLow"]
    range_ok = (h52 >= cur_price * 0.95) and (l52 <= cur_price * 1.05) and (h52 >= l52)
    checks.append(("52-Week High/Low Band Bounds", range_ok, f"52W Low=${l52} <= Current=${cur_price} <= 52W High=${h52}"))

    # 4. 기술적 지표 (RSI, MACD, 볼린저) 정밀도
    rsi = tech["rsi"]
    rsi_ok = 0.0 <= rsi <= 100.0
    checks.append(("Wilder's RSI(14) Bounds [0, 100]", rsi_ok, f"RSI = {rsi} ({tech['rsiSignal']})"))

    macd = tech["macd"]
    signal = tech["macdSignal"]
    hist = tech["macdHist"]
    macd_math_ok = abs((macd - signal) - hist) < 0.05
    checks.append(("MACD Formula (MACD - Signal = Hist)", macd_math_ok, f"MACD({macd}) - Signal({signal}) == Hist({hist})"))

    bb_u = tech["bollingerUpper"]
    bb_m = tech["bollingerMiddle"]
    bb_l = tech["bollingerLower"]
    bb_ok = bb_l <= bb_m <= bb_u
    checks.append(("Bollinger Bands Order (L <= M <= U)", bb_ok, f"Lower(${bb_l}) <= Middle(${bb_m}) <= Upper(${bb_u})"))

    # 5. 펀더멘털 & DCF 내재가치 수식 정합성
    dcf = fund["intrinsicValueDCF"]
    calc_upside = round(((dcf - cur_price) / cur_price) * 100, 2)
    upside_ok = abs(fund["upsidePotential"] - calc_upside) < 0.1
    checks.append(("DCF Upside Math Integrity", upside_ok, f"DCF=${dcf} -> Upside={fund['upsidePotential']}% (Calculated: {calc_upside}%)"))

    # 6. CIO 가중치 합성 점수 수학적 무결성
    f_score = committee["fundamental"]["score"]
    t_score = committee["technical"]["score"]
    s_score = committee["sentiment"]["score"]
    r_score = committee["risk"]["score"]
    expected_composite = round((f_score * 0.35) + (t_score * 0.25) + (s_score * 0.20) + (r_score * 0.20), 1)
    actual_composite = cio["compositeScore"]
    cio_math_ok = abs(expected_composite - actual_composite) < 0.15
    checks.append(("CIO 5-Agent Weighted Formula", cio_math_ok, f"FA({f_score}*0.35) + TA({t_score}*0.25) + SENT({s_score}*0.2) + RISK({r_score}*0.2) = {expected_composite} vs Actual={actual_composite}"))

    # 리포트 출력
    all_passed = True
    for name, ok, detail in checks:
        mark = "[PASS]" if ok else "[FAIL]"
        if not ok:
            all_passed = False
        print(f"{mark:<7} | {name:<35} | {detail}")

    print(f"\nFinal Verdict: {cio['recommendation']} (Target: ${cio['targetPrice']}, Expected Return: {cio['expectedReturn']}%)")
    print(f"Latency: {fetch_latency:.3f}s | Overall Integrity: {'100% PASSED' if all_passed else 'SOME FAILED'}")
    return all_passed

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# APEX TERMINAL - SYSTEM CONSISTENCY & ACCURACY AUDIT")
    print("#"*70)

    test_tickers = ["NVDA", "AAPL", "MSFT"]
    results = [verify_ticker_consistency(sym) for sym in test_tickers]

    print(f"\n{'='*70}")
    print(f"Audit Summary: {results.count(True)}/{len(test_tickers)} Tickers Passed 100% Consistency Checks!")
    print(f"{'='*70}\n")
