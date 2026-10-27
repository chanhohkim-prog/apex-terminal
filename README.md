# 🚀 Project Apex Terminal (Next-Gen AI Bloomberg)

> **"Wall Street Analyst in a Box"** — LLM API 키 없이도 즉시 동작하는 실시간 미국 주식 멀티 에이전트 투자 분석 터미널

링크드인과 X(트위터)에서 가장 핫한 **AI Financial Analyst / AI Hedge Fund** 아키텍처를 블룸버그 터미널 감성(Black & Amber)의 웹 대시보드로 완벽 구현한 시스템입니다.

---

## 🏛️ 시스템 아키텍처 & 멀티 에이전트 위원회

```
                                [ Ticker Input (e.g. NVDA, AAPL) ]
                                                │
                                                ▼
                        ┌────────────────────────────────────────────────┐
                        │        Data Layer (yfinance & SEC EDGAR)       │
                        │    - Real-time Price & OHLCV History           │
                        │    - Financial Statements & Valuation Multiples│
                        │    - Live News Headlines & Market Indices      │
                        └───────────────────────┬────────────────────────┘
                                                │
                                                ▼
                        ┌────────────────────────────────────────────────┐
                        │      Quantitative Math & Indicator Engine      │
                        │    - Technical: RSI(14), MACD, SMA, Bollinger  │
                        │    - Fundamental: DCF Intrinsic Value, Margin  │
                        │    - Risk: 1Y Max Drawdown (MDD), Beta, Sharpe │
                        └───────────────────────┬────────────────────────┘
                                                │
                 ┌──────────────┬───────────────┴───────────────┬──────────────┐
                 ▼              ▼                               ▼              ▼
        ┌────────────────┐ ┌────────────────┐         ┌────────────────┐ ┌────────────────┐
        │  📊 FUNDAMENTAL │ │  📈 TECHNICAL   │         │  📰 SENTIMENT  │ │   🛡️ RISK MGR   │
        │     ANALYST    │ │     ANALYST    │         │  & NEWS AGENT  │ │     AGENT      │
        │ (DCF/PER/Growth│ │(Momentum/Trend/│         │ (NLP Sentiment/│ │(MDD/Volatility/│
        │  Score 0-100)  │ │  Score 0-100)  │         │  Score 0-100)  │ │  Alloc & Stop) │
        └────────┬───────┘ └────────┬───────┘         └────────┬───────┘ └────────┬───────┘
                 │                  │                          │                  │
                 └──────────────────┼──────────────────────────┴──────────────────┘
                                    │
                                    ▼
                    ┌────────────────────────────────────────────────┐
                    │      👑 Chief Investment Officer (CIO) Agent   │
                    │   - Weighted Composite Score (0~100)           │
                    │   - Final Verdict: STRONG BUY / BUY / HOLD...  │
                    │   - 12M Target Price & Expected Return (%)     │
                    │   - Executive Board Investment Memo            │
                    └───────────────────────┬────────────────────────┘
                                            │
                                            ▼
                    ┌────────────────────────────────────────────────┐
                    │     🖥️ Bloomberg Style Web Terminal UI        │
                    │   - Real-time Global Ticker Tape Scroller      │
                    │   - Interactive Candlestick / Area Chart       │
                    │   - Command Bar: NVDA <GO>, TSLA <GO>          │
                    │   - Multi-Agent Tabs & Live News Feed          │
                    └────────────────────────────────────────────────┘
```

---

## 💡 차별화 포인트

1. **Zero-Key Zero-Cost (API 키 불필요)**:
   - 고가의 OpenAI/Anthropic 유료 토큰 없이도, 내장 퀀트 수식 엔진을 통해 정밀한 전문 애널리스트 수준의 리포트를 실시간 무제한 생성합니다.
2. **5인 멀티 에이전트 합의 알고리즘**:
   - 펀더멘털(35%), 테크니컬(25%), 센티먼트(20%), 리스크(20%)의 가중 평균으로 객관적이고 균형 잡힌 최종 투자 의결문(CIO Decision) 도출.
3. **블룸버그 특유의 시각적 카타르시스**:
   - Pitch Black 배경 + 시그니처 호박색(Amber `#FF9900`) + 네온 그린 포인트
   - 상단 실시간 글로벌 벤치마크 마켓 테이프(S&P500, 나스닥, 다우, VIX, 미10년물 국채, 비트코인)
   - 크로스헤어 십자선 & 거래량 볼륨 오버레이 인터랙티브 차트

---

## ⚡ 빠른 실행 방법 (One-Click)

### 방법 1: 원클릭 실행 (가장 추천)
프로젝트 루트의 **`start.bat`** 파일을 더블클릭하면 백엔드, 프론트엔드, 브라우저가 자동으로 켜집니다!

### 방법 2: 수동 실행
**1. 백엔드 (FastAPI)**
```bash
cd backend
.\venv\Scripts\python run.py
# Server runs on: http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
```

**2. 프론트엔드 (Next.js)**
```bash
cd frontend
npm run dev
# Dashboard runs on: http://localhost:3000
```

---

## ⌨️ 사용 예시
- 커맨드 바에 `NVDA` 입력 후 `<GO>` 클릭 (또는 상단 단축 버튼 클릭)
- 1초 만에 최신 주가, 캔들 차트, 4개 전문 에이전트 점수 및 CIO 의결문 스트리밍 확인!
