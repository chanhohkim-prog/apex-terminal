from typing import Dict, Any

def run_fundamental_agent(overview: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fundamental Analyst Agent:
    Evaluates valuation, earnings quality, balance sheet health, and DCF intrinsic value.
    Returns: Score (0-100), Verdict, Key Bullets, and Detailed Analysis Report.
    """
    score = 50
    pros = []
    cons = []

    pe = overview.get("peRatio", 0)
    peg = overview.get("pegRatio", 0)
    upside = metrics.get("upsidePotential", 0)
    roe = metrics.get("roe", 0)
    profit_margin = metrics.get("profitMargins", 0)
    rev_growth = metrics.get("revenueGrowth", 0)
    debt_equity = metrics.get("debtToEquity", 0)
    intrinsic_val = metrics.get("intrinsicValueDCF", 0)
    current_price = overview.get("currentPrice", 0)

    # 1. Valuation Evaluation
    if 0 < pe < 22:
        score += 15
        pros.append(f"PER {pe}x로 동종업계 대비 매력적인 밸류에이션 구간")
    elif pe >= 45:
        score -= 10
        cons.append(f"PER {pe}x로 단기 밸류에이션 부담 상존")
    elif pe <= 0:
        score -= 15
        cons.append("현재 적자 상태로 전통적 PER 산출 불가")

    if 0 < peg < 1.5:
        score += 10
        pros.append(f"PEG {peg}로 이익 성장성 대비 저평가 영역")
    elif peg > 2.5:
        score -= 8
        cons.append(f"PEG {peg}로 성장성 대비 프리미엄이 높게 반영됨")

    # 2. Growth & Profitability
    if rev_growth > 15:
        score += 10
        pros.append(f"매출 성장률 {rev_growth}%로 강력한 외형 확장 지속")
    elif rev_growth < 0:
        score -= 10
        cons.append(f"매출 성장률 {rev_growth}%로 역성장 신호")

    if roe > 20:
        score += 10
        pros.append(f"ROE {roe}%로 뛰어난 자기자본 이익창출력 증명")
    elif roe < 5:
        score -= 8
        cons.append(f"ROE {roe}%로 자본 효율성이 다소 부진")

    if profit_margin > 20:
        score += 8
        pros.append(f"순이익률 {profit_margin}%로 두터운 마진 해자 보유")

    # 3. DCF Fair Value Upside
    if upside > 20:
        score += 10
        pros.append(f"DCF 산출 적정가(${intrinsic_val}) 대비 현주가(${current_price}) +{upside}% 상승 여력")
    elif upside < -15:
        score -= 8
        cons.append(f"DCF 산출 적정가 대비 현주가가 {abs(upside)}% 고평가 상태")

    # Clamp score
    score = max(10, min(95, score))

    if score >= 75:
        verdict = "STRONG VALUE & GROWTH (강력 펀더멘털)"
    elif score >= 55:
        verdict = "MODERATE (안정적 펀더멘털)"
    else:
        verdict = "WEAK (펀더멘털 경고/고평가)"

    report = (
        f"【펀더멘털 분석 총평】\n"
        f"현재 주가는 ${current_price}이며, DCF 기반 내재가치는 ${intrinsic_val} (상승여력 {upside:+.1f}%)로 추정됩니다. "
        f"매출 성장률({rev_growth}%)과 순이익률({profit_margin}%)을 종합할 때 사업 펀더멘털의 체력은 {metrics.get('healthStatus')} 등급입니다. "
        f"ROE {roe}%와 부채비율 {debt_equity}% 수준을 감안 시 중장기 현금창출능력은 우수한 편입니다."
    )

    return {
        "agent": "Fundamental Analyst",
        "score": score,
        "verdict": verdict,
        "intrinsicValue": intrinsic_val,
        "upside": upside,
        "pros": pros,
        "cons": cons,
        "report": report
    }
