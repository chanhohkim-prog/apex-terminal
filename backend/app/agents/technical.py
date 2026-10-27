from typing import Dict, Any

def run_technical_agent(overview: Dict[str, Any], tech: Dict[str, Any]) -> Dict[str, Any]:
    """
    Technical Analyst Agent:
    Evaluates momentum, moving average trends, RSI, MACD, and Bollinger band positioning.
    Returns: Score (0-100), Verdict, Key Bullets, and Detailed Chart Commentary.
    """
    score = 50
    pros = []
    cons = []

    rsi = tech.get("rsi", 50.0)
    macd_trend = tech.get("macdTrend", "NEUTRAL")
    macd_hist = tech.get("macdHist", 0.0)
    golden_cross = tech.get("goldenCross", False)
    death_cross = tech.get("deathCross", False)
    sma20 = tech.get("sma20", 0.0)
    sma50 = tech.get("sma50", 0.0)
    sma200 = tech.get("sma200", 0.0)
    price = overview.get("currentPrice", 0.0)
    bb_upper = tech.get("bollingerUpper", 0.0)
    bb_lower = tech.get("bollingerLower", 0.0)

    # 1. Moving Average Alignment
    if price > sma20 > sma50 > sma200:
        score += 20
        pros.append("주가 및 단/중/장기 이동평균선(20/50/200) 완벽한 정배열 상승추세")
    elif price < sma20 < sma50:
        score -= 15
        cons.append("단기 및 중기 이평선 아래로 주가 하회 (역배열 하락압력)")

    if golden_cross:
        score += 15
        pros.append("50일선이 200일선을 상향 돌파하는 강력한 골든크로스(Golden Cross) 발생!")
    elif death_cross:
        score -= 15
        cons.append("데드크로스(Death Cross) 경고: 중장기 추세 약화 국면 진입")

    # 2. RSI Signal
    if 45 <= rsi <= 65:
        score += 5
        pros.append(f"RSI {rsi}로 과열/과매도 없는 건전한 모멘텀 구간")
    elif rsi > 75:
        score -= 10
        cons.append(f"RSI {rsi}로 극심한 과매수(Overbought) 구간 진입 - 단기 차익실현 매물 주의")
    elif rsi < 30:
        score += 10
        pros.append(f"RSI {rsi}로 역사적 과매도(Oversold) 구간 - 기술적 반등 매수세 유입 가능")

    # 3. MACD
    if "BULLISH" in macd_trend:
        score += 10
        pros.append(f"MACD 시그널선 상회 및 양(+)의 히스토그램({macd_hist})으로 상승 모멘텀 유지")
    else:
        score -= 10
        cons.append("MACD 시그널선 하회로 단기 모멘텀 둔화 신호")

    # 4. Bollinger Bands
    if price > bb_upper:
        cons.append(f"볼린저밴드 상단(${bb_upper}) 돌파로 단기 이격도 과대")
    elif price < bb_lower:
        pros.append(f"볼린저밴드 하단(${bb_lower}) 지지선 부근으로 반등 기대치 상승")

    score = max(10, min(95, score))

    if score >= 70:
        verdict = "STRONG BULLISH (강력 매수 모멘텀)"
    elif score >= 50:
        verdict = "NEUTRAL CONSOLIDATION (박스권 횡보)"
    else:
        verdict = "BEARISH (하락 추세/관망)"

    report = (
        f"【기술적 분석 총평】\n"
        f"현재 주가는 ${price}로 20일선(${sma20})과 50일선(${sma50}) 대비 "
        f"{'상회하며 견조한' if price >= sma50 else '하회하며 조정'} 양상을 보입니다. "
        f"RSI는 {rsi}로 {tech.get('rsiSignal')}이며, MACD는 {macd_trend} 상태입니다. "
        f"단기 저항선은 볼린저 상단(${bb_upper}), 지지선은 볼린저 하단(${bb_lower})으로 설정됩니다."
    )

    return {
        "agent": "Technical Analyst",
        "score": score,
        "verdict": verdict,
        "rsi": rsi,
        "pros": pros,
        "cons": cons,
        "report": report
    }
