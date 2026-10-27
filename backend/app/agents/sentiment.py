from typing import Dict, Any, List

BULLISH_KEYWORDS = [
    "surge", "jump", "record", "beat", "rally", "upgrade", "outperform", "growth",
    "profit", "strong", "bull", "partnership", "breakthrough", "higher", "gain", "buy",
    "상승", "돌파", "호실적", "최고치", "매수"
]

BEARISH_KEYWORDS = [
    "plunge", "drop", "fall", "miss", "downgrade", "underperform", "slump", "loss",
    "lawsuit", "investigation", "weak", "bear", "recession", "lower", "warning", "sell",
    "하락", "폭락", "부진", "경고", "소송"
]

def run_sentiment_agent(overview: Dict[str, Any], news: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Sentiment & News Analyst Agent:
    Evaluates market sentiment from analyst consensus and news headline NLP keywords.
    """
    score = 50
    bullish_count = 0
    bearish_count = 0
    analyzed_headlines = []

    # 1. News Headline Keyword Sentiment
    for item in news:
        title = item.get("title", "").lower()
        is_bull = any(kw in title for kw in BULLISH_KEYWORDS)
        is_bear = any(kw in title for kw in BEARISH_KEYWORDS)
        
        sentiment_tag = "NEUTRAL"
        if is_bull and not is_bear:
            bullish_count += 1
            sentiment_tag = "POSITIVE"
        elif is_bear and not is_bull:
            bearish_count += 1
            sentiment_tag = "NEGATIVE"
            
        analyzed_headlines.append({
            "title": item.get("title"),
            "publisher": item.get("publisher"),
            "sentiment": sentiment_tag,
            "link": item.get("link")
        })

    total_tagged = bullish_count + bearish_count
    if total_tagged > 0:
        net_sentiment = (bullish_count - bearish_count) / total_tagged
        score += int(net_sentiment * 25)

    # 2. Wall Street Consensus
    consensus = overview.get("recommendationKey", "NONE")
    opinions_num = overview.get("numberOfAnalystOpinions", 0)

    if consensus in ["STRONG_BUY", "BUY"]:
        score += 15
    elif consensus in ["OVERPERFORM"]:
        score += 10
    elif consensus in ["UNDERPERFORM", "SELL"]:
        score -= 15

    score = max(10, min(95, score))

    if score >= 65:
        verdict = "GREED / HIGH SENTIMENT (강한 낙관론)"
    elif score >= 45:
        verdict = "BALANCED SENTIMENT (균형적 심리)"
    else:
        verdict = "FEAR / NEGATIVE SENTIMENT (비관론 우세)"

    pros = []
    cons = []
    if bullish_count > 0:
        pros.append(f"최근 {len(news)}개 주요 뉴스 중 {bullish_count}건의 긍정적 촉매제(호재) 포착")
    if consensus in ["BUY", "STRONG_BUY"]:
        pros.append(f"월가 투자은행(IB) {opinions_num}개 기관의 평균 투자의견: '{consensus}'")
    if bearish_count > 0:
        cons.append(f"최근 뉴스 중 {bearish_count}건의 우려/악재 헤드라인 감지")

    report = (
        f"【센티먼트 & 뉴스 분석 총평】\n"
        f"최신 주요 뉴스 {len(news)}건 중 긍정 헤드라인 {bullish_count}건, 부정 헤드라인 {bearish_count}건으로 집계되었습니다. "
        f"월스트리트 {opinions_num}개 기관의 컨센서스는 '{consensus}'이며, "
        f"시장 전반의 심리는 {verdict} 상태를 유지하고 있습니다."
    )

    return {
        "agent": "Sentiment & News Analyst",
        "score": score,
        "verdict": verdict,
        "bullishArticles": bullish_count,
        "bearishArticles": bearish_count,
        "analystConsensus": consensus,
        "pros": pros,
        "cons": cons,
        "report": report,
        "headlines": analyzed_headlines[:5]
    }
