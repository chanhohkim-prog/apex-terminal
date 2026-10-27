from typing import Dict, Any

def run_cio_agent(
    overview: Dict[str, Any],
    fundamental: Dict[str, Any],
    technical: Dict[str, Any],
    sentiment: Dict[str, Any],
    risk: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Chief Investment Officer (CIO) / Lead Analyst Agent:
    Synthesizes the evaluations from Fundamental, Technical, Sentiment, and Risk agents.
    Computes a weighted composite score, final investment decision, and target price.
    """
    f_score = fundamental.get("score", 50)
    t_score = technical.get("score", 50)
    s_score = sentiment.get("score", 50)
    r_score = risk.get("score", 50)

    # Weights: Fundamental 35%, Technical 25%, Sentiment 20%, Risk 20%
    composite_score = round(
        (f_score * 0.35) +
        (t_score * 0.25) +
        (s_score * 0.20) +
        (r_score * 0.20),
        1
    )

    # Determine final recommendation
    if composite_score >= 80:
        recommendation = "STRONG BUY (강력 매수)"
        action_color = "#00FF66" # Neon green
    elif composite_score >= 65:
        recommendation = "BUY (매수)"
        action_color = "#33CC66"
    elif composite_score >= 48:
        recommendation = "HOLD (중립/보유)"
        action_color = "#FF9900" # Bloomberg Amber
    elif composite_score >= 35:
        recommendation = "UNDERWEIGHT (비중 축소)"
        action_color = "#FF5533"
    else:
        recommendation = "STRONG SELL (적극 매도)"
        action_color = "#FF0033" # Red

    current_price = overview.get("currentPrice", 0.0)
    intrinsic_val = fundamental.get("intrinsicValue", current_price)
    target_mean = overview.get("targetMeanPrice", 0.0)

    # Blend intrinsic valuation with consensus target
    if target_mean > 0 and intrinsic_val > 0:
        composite_target = round((intrinsic_val * 0.6) + (target_mean * 0.4), 2)
    elif intrinsic_val > 0:
        composite_target = intrinsic_val
    elif target_mean > 0:
        composite_target = target_mean
    else:
        composite_target = round(current_price * 1.1, 2)

    expected_return = round(((composite_target - current_price) / current_price * 100), 2) if current_price > 0 else 0.0

    executive_summary = (
        f"【투자위원회(CIO) 최종 의결문】\n"
        f"투자위원회는 {overview.get('name')}({overview.get('symbol')})에 대해 "
        f"종합 점수 {composite_score}/100점으로 [{recommendation}] 의견을 승인합니다.\n\n"
        f"• 목표 주가: ${composite_target} (현주가 대비 기대 수익률 {expected_return:+.1f}%)\n"
        f"• 펀더멘털 평가: {fundamental.get('verdict')} (점수: {f_score})\n"
        f"• 차트/모멘텀 평가: {technical.get('verdict')} (점수: {t_score})\n"
        f"• 시장 센티먼트: {sentiment.get('verdict')} (점수: {s_score})\n"
        f"• 리스크/포지션: {risk.get('riskGrade')} (점수: {r_score}, 권장 비중 {risk.get('portfolioAllocation')})\n\n"
        f"전략 제언: {fundamental.get('pros')[0] if fundamental.get('pros') else '사업 경쟁력 주시'} "
        f"차트 측면에서는 {technical.get('pros')[0] if technical.get('pros') else '지지선 유지 관망'}을(를) 확인하며, "
        f"손절 기준가 ${risk.get('suggestedStopLoss')}를 설정한 단계적 분할 접근을 권고합니다."
    )

    return {
        "agent": "Chief Investment Officer",
        "compositeScore": composite_score,
        "recommendation": recommendation,
        "actionColor": action_color,
        "targetPrice": composite_target,
        "expectedReturn": expected_return,
        "executiveSummary": executive_summary,
        "agentScores": {
            "fundamental": f_score,
            "technical": t_score,
            "sentiment": s_score,
            "risk": r_score
        }
    }
