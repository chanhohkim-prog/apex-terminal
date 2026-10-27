"use client";

import React, { useState, useEffect } from "react";
import TickerTape from "@/components/TickerTape";
import PriceChart from "@/components/PriceChart";
import AgentCommittee from "@/components/AgentCommittee";
import API_BASE_URL from "@/config";
import {
  Terminal,
  Clock,
  Radio,
  ExternalLink,
  Globe,
  Loader2,
  TrendingUp,
  TrendingDown,
  Zap,
  Star,
  RefreshCw,
  Database,
  History,
  X
} from "lucide-react";

const DEFAULT_TICKERS = ["NVDA", "AAPL", "TSLA", "MSFT", "AMZN", "PLTR"];

export default function TerminalHome() {
  const [currentSymbol, setCurrentSymbol] = useState("NVDA");
  const [inputSymbol, setInputSymbol] = useState("");
  const [period, setPeriod] = useState("1y");

  const [overview, setOverview] = useState<any>(null);
  const [chartData, setChartData] = useState<any[]>([]);
  const [news, setNews] = useState<any[]>([]);
  const [committee, setCommittee] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [currentTime, setCurrentTime] = useState("");
  const [fetchLatency, setFetchLatency] = useState<number | null>(null);

  // Watchlist & History state
  const [watchlist, setWatchlist] = useState<string[]>([]);
  const [historyLogs, setHistoryLogs] = useState<any[]>([]);
  const [showHistoryModal, setShowHistoryModal] = useState(false);

  // Live Clock
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(
        now.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false,
        })
      );
    };
    updateTime();
    const t = setInterval(updateTime, 1000);
    return () => clearInterval(t);
  }, []);

  // Fetch Watchlist from SQLite
  const loadWatchlist = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/market/watchlist`);
      if (res.ok) {
        const data = await res.json();
        setWatchlist(data.symbols || []);
      }
    } catch (e) {
      console.error("Failed to load watchlist", e);
    }
  };

  useEffect(() => {
    loadWatchlist();
  }, []);

  // ⚡ ULTRA-FAST SINGLE-TRIP FETCH (With SQLite Local DB Cache)
  const loadTickerData = async (sym: string, per: string, force: boolean = false) => {
    if (force) setRefreshing(true);
    else setLoading(true);

    const t0 = performance.now();
    try {
      const url = `${API_BASE_URL}/api/analysis/deep-dive/${sym}?period=${per}&force_refresh=${force}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setOverview(data.overview);
        setChartData(data.chartData || []);
        setNews(data.news || []);
        setCommittee(data.committee);
        setFetchLatency(Math.round(performance.now() - t0));
      }
    } catch (e) {
      console.error("Error loading ticker analysis", e);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadTickerData(currentSymbol, period);
  }, [currentSymbol, period]);

  // Toggle Watchlist
  const handleToggleWatchlist = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/market/watchlist/${currentSymbol}`, {
        method: "POST"
      });
      if (res.ok) {
        const data = await res.json();
        setWatchlist(data.allSymbols || []);
      }
    } catch (e) {
      console.error("Failed to toggle watchlist", e);
    }
  };

  // Open Analysis History Modal
  const openHistoryModal = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/analysis/history/${currentSymbol}`);
      if (res.ok) {
        const data = await res.json();
        setHistoryLogs(data);
        setShowHistoryModal(true);
      }
    } catch (e) {
      console.error("Failed to load history", e);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputSymbol.trim()) {
      const sym = inputSymbol.toUpperCase().trim();
      setCurrentSymbol(sym);
      setInputSymbol("");
    }
  };

  const isUp = overview ? overview.change >= 0 : true;
  const isInWatchlist = watchlist.includes(currentSymbol);

  return (
    <div className="flex flex-col min-h-screen bg-[#07090e] text-[#d6deeb] font-sans">
      {/* 1. Global Ticker Tape */}
      <TickerTape />

      {/* 2. Bloomberg Header Bar */}
      <header className="bg-[#0b0e17] border-b border-[#1b2133] px-4 py-2 flex flex-wrap items-center justify-between gap-3 font-mono">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5 text-[#ff9900]">
            <Terminal className="w-5 h-5" />
            <span className="font-black text-lg tracking-wider">APEX TERMINAL</span>
            <span className="text-[10px] text-gray-400 border border-gray-700 px-1.5 py-0.2 rounded">
              v2.5 SQLITE-HYBRID
            </span>
          </div>

          <div className="hidden md:flex items-center space-x-3 text-xs text-gray-400 pl-4 border-l border-[#1b2133]">
            <span className="flex items-center space-x-1 text-[#00ff66]">
              <Database className="w-3.5 h-3.5" />
              <span>PERSISTENT LOCAL DB</span>
            </span>
            {fetchLatency !== null && (
              <span className="flex items-center space-x-1 text-[#ff9900] bg-[#ff9900]/10 px-2 py-0.5 rounded border border-[#ff9900]/20 text-[11px]">
                <Zap className="w-3 h-3" />
                <span>{fetchLatency}ms</span>
              </span>
            )}
          </div>
        </div>

        {/* Bloomberg Command Prompt Search Bar */}
        <form onSubmit={handleSearch} className="flex items-center flex-1 max-w-md mx-2">
          <div className="relative w-full">
            <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-[#ff9900] font-bold text-xs pointer-events-none">
              &gt;
            </span>
            <input
              type="text"
              value={inputSymbol}
              onChange={(e) => setInputSymbol(e.target.value)}
              placeholder="ENTER TICKER (e.g. NVDA, TSLA, AAPL) <GO>"
              className="w-full bg-[#121624] border border-[#232a40] focus:border-[#ff9900] focus:outline-none rounded pl-8 pr-16 py-1.5 text-xs text-white uppercase placeholder-gray-500 font-mono"
            />
            <button
              type="submit"
              className="absolute inset-y-0 right-1 my-1 px-2.5 bg-[#ff9900] hover:bg-[#e68a00] text-black font-bold text-xs rounded transition-colors"
            >
              &lt;GO&gt;
            </button>
          </div>
        </form>

        {/* Watchlist & Default Tickers */}
        <div className="flex items-center space-x-2 text-xs">
          <div className="hidden lg:flex items-center space-x-1">
            {/* Show Watchlist items first if any, otherwise default */}
            {(watchlist.length > 0 ? watchlist.slice(0, 6) : DEFAULT_TICKERS).map((t) => (
              <button
                key={t}
                onClick={() => setCurrentSymbol(t)}
                className={`px-2 py-0.5 rounded transition-colors ${
                  currentSymbol === t
                    ? "bg-[#ff9900] text-black font-bold"
                    : "bg-[#141827] text-gray-400 hover:text-white border border-[#21273c]"
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          <div className="flex items-center space-x-1.5 text-gray-400 bg-[#121624] border border-[#232a40] px-2.5 py-1 rounded">
            <Clock className="w-3.5 h-3.5 text-[#ff9900]" />
            <span className="font-mono">{currentTime || "LIVE"}</span>
          </div>
        </div>
      </header>

      {/* 3. Ticker Overview Headline Card */}
      {overview && (
        <section className="bg-[#0c0f1a] border-b border-[#1b2133] px-4 py-2.5 font-mono">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-4">
              <div>
                <div className="flex items-center space-x-2">
                  <h1 className="text-2xl font-black text-white tracking-tight flex items-center space-x-2">
                    <span>{overview.symbol}</span>
                    <button
                      onClick={handleToggleWatchlist}
                      title={isInWatchlist ? "Remove from Watchlist" : "Save to Watchlist"}
                      className={`p-1 rounded transition-colors ${
                        isInWatchlist ? "text-[#ff9900]" : "text-gray-600 hover:text-gray-300"
                      }`}
                    >
                      <Star className={`w-4 h-4 ${isInWatchlist ? "fill-[#ff9900]" : ""}`} />
                    </button>
                  </h1>
                  <span className="text-xs text-gray-400 font-normal">
                    {overview.name}
                  </span>
                  <span className="text-[10px] bg-[#1a2033] text-gray-300 px-2 py-0.5 rounded border border-[#2c3552]">
                    {overview.sector} // {overview.industry}
                  </span>

                  {/* DB Cache Badge */}
                  {overview.isDbCached && (
                    <span className="text-[10px] bg-[#00ff66]/10 text-[#00ff66] px-1.5 py-0.5 rounded border border-[#00ff66]/20 flex items-center space-x-1">
                      <Database className="w-3 h-3" />
                      <span>DB CACHE ({overview.cacheAgeSeconds}s ago)</span>
                    </span>
                  )}
                </div>

                <div className="flex items-baseline space-x-3 mt-1">
                  <span className="text-3xl font-black text-white">
                    ${overview.currentPrice?.toFixed(2)}
                  </span>
                  <span
                    className={`flex items-center space-x-1 font-bold text-sm ${
                      isUp ? "text-[#00ff66]" : "text-[#ff3344]"
                    }`}
                  >
                    {isUp ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    <span>
                      {isUp ? "+" : ""}
                      {overview.change?.toFixed(2)} ({isUp ? "+" : ""}
                      {overview.changePct?.toFixed(2)}%)
                    </span>
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Metrics Bar & Actions */}
            <div className="flex items-center space-x-6">
              <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-x-6 gap-y-2 text-xs">
                <div>
                  <span className="text-gray-500 block text-[10px]">MARKET CAP</span>
                  <span className="text-white font-bold">
                    {overview.marketCap ? `$${(overview.marketCap / 1e12).toFixed(2)}T` : "N/A"}
                  </span>
                </div>
                <div>
                  <span className="text-gray-500 block text-[10px]">P/E (TTM)</span>
                  <span className="text-white font-bold">{overview.peRatio ? `${overview.peRatio}x` : "N/A"}</span>
                </div>
                <div>
                  <span className="text-gray-500 block text-[10px]">FORWARD P/E</span>
                  <span className="text-white font-bold">{overview.forwardPE ? `${overview.forwardPE}x` : "N/A"}</span>
                </div>
                <div>
                  <span className="text-gray-500 block text-[10px]">BETA</span>
                  <span className="text-white font-bold">{overview.beta || "1.0"}</span>
                </div>
                <div>
                  <span className="text-gray-500 block text-[10px]">52W HIGH / LOW</span>
                  <span className="text-white font-bold">
                    ${overview.fiftyTwoWeekHigh} / ${overview.fiftyTwoWeekLow}
                  </span>
                </div>
                <div>
                  <span className="text-gray-500 block text-[10px]">CONSENSUS</span>
                  <span className="text-[#ff9900] font-bold">
                    {overview.recommendationKey || "BUY"}
                  </span>
                </div>
              </div>

              {/* Force Refresh & History Buttons */}
              <div className="flex items-center space-x-2 pl-4 border-l border-[#1b2133]">
                <button
                  onClick={() => loadTickerData(currentSymbol, period, true)}
                  disabled={refreshing}
                  title="Force Live Network Sync"
                  className="p-2 rounded bg-[#131724] hover:bg-[#1b2133] border border-[#22283a] text-gray-300 hover:text-[#ff9900] transition-colors"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? "animate-spin text-[#ff9900]" : ""}`} />
                </button>
                <button
                  onClick={openHistoryModal}
                  title="View Past AI Audit Logs"
                  className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded bg-[#131724] hover:bg-[#1b2133] border border-[#22283a] text-xs font-mono text-gray-300 hover:text-white transition-colors"
                >
                  <History className="w-3.5 h-3.5 text-[#ff9900]" />
                  <span>AUDIT LOGS</span>
                </button>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* 4. Main Body: Left (Chart & News) + Right (AI Committee Panel) */}
      <main className="flex-1 p-4 grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left Column (7 cols): Interactive Chart & News */}
        <div className="lg:col-span-7 flex flex-col space-y-4">
          <div className="flex-1 min-h-[420px]">
            <PriceChart
              symbol={currentSymbol}
              chartData={chartData}
              onPeriodChange={(newPeriod) => setPeriod(newPeriod)}
              currentPeriod={period}
            />
          </div>

          {/* Live News Feed Card */}
          <div className="bg-[#0e111a] border border-[#1e2335] rounded-lg p-4 font-mono">
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-[#1c2132]">
              <div className="flex items-center space-x-2 text-sm font-bold text-white">
                <Globe className="w-4 h-4 text-[#ff9900]" />
                <span>TERMINAL WIRE NEWS // {currentSymbol}</span>
              </div>
              <span className="text-[10px] text-gray-500">LIVE HEADLINE NLP</span>
            </div>

            <div className="space-y-2 max-h-[200px] overflow-y-auto pr-1">
              {news.map((item, idx) => (
                <div
                  key={idx}
                  className="bg-[#090b12] hover:bg-[#121625] transition-colors p-2 rounded border border-[#1a1f2e] flex items-start justify-between gap-3 text-xs"
                >
                  <div className="space-y-0.5">
                    <p className="text-gray-200 hover:text-[#ff9900] font-medium leading-snug cursor-pointer">
                      {item.title}
                    </p>
                    <div className="flex items-center space-x-2 text-[10px] text-gray-500">
                      <span className="text-[#ff9900]">{item.publisher}</span>
                      <span>•</span>
                      <span>{item.time}</span>
                    </div>
                  </div>
                  <a
                    href={item.link}
                    target="_blank"
                    rel="noreferrer"
                    className="text-gray-500 hover:text-white p-1"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column (5 cols): AI Multi-Agent Committee */}
        <div className="lg:col-span-5 flex flex-col space-y-4">
          {loading ? (
            <div className="bg-[#0e111a] border border-[#1e2335] rounded-lg p-12 flex flex-col items-center justify-center space-y-4 text-center h-full">
              <Loader2 className="w-10 h-10 text-[#ff9900] animate-spin" />
              <div>
                <h3 className="text-base font-bold text-white font-mono">
                  AI INVESTMENT COMMITTEE CONVENING...
                </h3>
                <p className="text-xs text-gray-400 font-mono mt-1">
                  Parsing Wilder RSI, DCF Intrinsic Model & Risk Management
                </p>
              </div>
            </div>
          ) : committee ? (
            <AgentCommittee committee={committee} />
          ) : (
            <div className="text-center p-8 text-gray-500 font-mono">
              No Committee analysis available.
            </div>
          )}
        </div>
      </main>

      {/* 5. Analysis History Audit Modal */}
      {showHistoryModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0f121b] border border-[#22293d] rounded-xl max-w-2xl w-full max-h-[80vh] flex flex-col shadow-2xl font-mono">
            <div className="p-4 border-b border-[#1f2638] flex items-center justify-between">
              <div className="flex items-center space-x-2 text-white font-bold text-base">
                <History className="w-5 h-5 text-[#ff9900]" />
                <span>AI AUDIT TRAIL // {currentSymbol}</span>
              </div>
              <button
                onClick={() => setShowHistoryModal(false)}
                className="text-gray-400 hover:text-white p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 overflow-y-auto space-y-3 flex-1">
              {historyLogs.length === 0 ? (
                <div className="text-center py-8 text-gray-500 text-xs">
                  No historical AI audit records for {currentSymbol} yet.
                </div>
              ) : (
                historyLogs.map((log) => (
                  <div
                    key={log.id}
                    className="bg-[#0a0d14] border border-[#1d2334] p-3 rounded-lg text-xs space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400 font-medium">{log.timeFormatted}</span>
                      <span className="font-bold text-[#ff9900]">
                        SCORE: {log.score}/100
                      </span>
                    </div>
                    <div className="flex items-center justify-between border-t border-[#1a2030] pt-2 text-gray-300">
                      <span>DECISION: <strong className="text-white">{log.recommendation}</strong></span>
                      <span>TARGET: <strong className="text-white">${log.targetPrice}</strong></span>
                      <span>EXP. RETURN: <strong className="text-[#00ff66]">{log.expectedReturn}%</strong></span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* 6. Terminal Footer Console */}
      <footer className="bg-[#090b12] border-t border-[#191e2c] px-4 py-2 flex flex-wrap items-center justify-between text-[11px] font-mono text-gray-500">
        <div className="flex items-center space-x-4">
          <span className="text-[#ff9900] font-bold">● SYSTEM OPERATIONAL</span>
          <span>STORAGE: SQLite 3 PERSISTENT CACHE</span>
          <span>ENGINE: WILDER'S RSI & 2-STAGE DCF GORDON</span>
        </div>
        <div className="text-gray-400">
          PROJECT APEX TERMINAL // NEXT-GEN AI BLOOMBERG
        </div>
      </footer>
    </div>
  );
}
