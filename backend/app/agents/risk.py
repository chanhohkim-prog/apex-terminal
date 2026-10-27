from typing import Dict, Any

def run_risk_agent(overview: Dict[str, Any], tech: Dict[str, Any]) -> Dict[str, Any]:
    """
    Risk Management Agent:
    Evaluates Beta, Annualized Volatility, Max Drawdown (MDD), and Sharpe Ratio.
    Provides suggested Stop-Loss level and recommended Portfolio Allocation (%).
    """
    beta = overview.get("beta", 1.0)
    volatility = tech.get("volatility", 25.0)
    mdd = tech.get("mdd", 20.0)
    sharpe = tech.get("sharpeRatio", 1.0)
    current_price = overview.get("currentPrice", 0.0)

    # Risk Score: High score means LOW risk / HIGH safety.
    # Low score means HIGH risk / CAUTION.
    score = 60
    pros = []
    cons = []

    # 1. Beta evaluation
    if beta < 0.9:
        score += 10
        pros.append(f"시장 대비 낮은 민감도 (Beta {beta})로 하락장 방어력 우수")
    elif beta > 1.5:
        score -= 10
        cons.append(f"고변동성 종목 (Beta {beta}): 지수 대비 급등락 리스크 주의")

    # 2. Volatility
    if volatility > 40:
        score -= 15
        cons.append(f"연환산 변동성 {volatility}%로 단기 가격 충격 가능성 상존")
    elif volatility < 25:
        score += 10
        pros.append(f"연환산 변동성 {volatility}%로 비교적 안정적인 주가 궤적")

    # 3. MDD (Max Drawdown)
    if mdd > 35:
        score -= 10
        cons.append(f"최근 1년 최대 낙폭(MDD) -{mdd}% 기록: 깊은 가격 조정 이력 확인")
    else:
        pros.append(f"최근 1년 최대 낙폭(MDD) -{mdd}%로 하방 경직성 확보")

    # 4. Sharpe Ratio
    if sharpe > 1.2:
        score += 10
        pros.append(f"샤프지수 {sharpe}로 변동성 대비 초과 수익 창출력 매우 우수")
    elif sharpe < 0.3:
        score -= 10
        cons.append(f"샤프지수 {sharpe}로 무위험 수익률 대비 위험 보상 비율 미흡")

    score = max(10, min(95, score))

    # Suggested Stop-Loss (e.g. 2x ATR or ~7-10% below current price)
    suggested_stop_loss = round(current_price * 0.92, 2)
    
    # Portfolio Allocation recommendation based on volatility and score
    if volatility > 45 or score < 40:
        alloc_recommendation = "2% ~ 4% (소액 분할 매수 / 헤지 필수)"
        risk_grade = "HIGH RISK (고위험)"
    elif volatility > 28 or score < 65:
        alloc_recommendation = "5% ~ 10% (표준 비중 편입)"
        risk_grade = "MODERATE RISK (중위험)"
    else:
        alloc_recommendation = "10% ~ 15% (핵심 코어 자산 편입 가능)"
        risk_grade = "LOW / STABLE RISK (저위험/안정)"

    report = (
        f"【리스크 관리자 총평】\n"
        f"해당 종목의 리스크 등급은 {risk_grade}입니다. "
        f"Beta {beta}, 연환산 변동성 {volatility}%, 1년 MDD -{mdd}%를 감안할 때, "
        f"권장 포트폴리오 편입 비중은 [{alloc_recommendation}]이며, "
        f"기술적 1차 방어 손절라인(Stop-Loss)은 ${suggested_stop_loss}로 설정하는 것을 권고합니다."
    )

    return {
        "agent": "Risk Manager",
        "score": score,
        "riskGrade": risk_grade,
        "beta": beta,
        "volatility": volatility,
        "mdd": mdd,
        "sharpeRatio": sharpe,
        "suggestedStopLoss": suggested_stop_loss,
        "portfolioAllocation": alloc_recommendation,
        "pros": pros,
        "cons": cons,
        "report": report
    }
