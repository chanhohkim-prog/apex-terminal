"use client";

import React, { useEffect, useState } from "react";
import { TrendingUp, TrendingDown, RefreshCw } from "lucide-react";

import API_BASE_URL from "@/config";

interface IndexItem {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePct: number;
}

export default function TickerTape() {
  const [indices, setIndices] = useState<IndexItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchIndices = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/market/indices`);
      if (res.ok) {
        const data = await res.json();
        setIndices(data);
      }
    } catch (e) {
      console.error("Failed to load ticker tape", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIndices();
    const interval = setInterval(fetchIndices, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full bg-[#0d0f17] border-b border-[#1f2433] px-3 py-1.5 flex items-center justify-between text-xs font-mono overflow-x-auto no-scrollbar">
      <div className="flex items-center space-x-6 min-w-max">
        <span className="flex items-center text-[#ff9900] font-bold tracking-wider px-2 py-0.5 rounded bg-[#ff9900]/10 border border-[#ff9900]/30">
          MARKETS LIVE
        </span>
        {indices.map((idx) => {
          const isUp = idx.change >= 0;
          return (
            <div key={idx.symbol} className="flex items-center space-x-2">
              <span className="text-gray-400 font-semibold">{idx.name}</span>
              <span className="text-white font-medium">{idx.price.toLocaleString()}</span>
              <span
                className={`flex items-center space-x-0.5 font-bold ${
                  isUp ? "text-[#00ff66]" : "text-[#ff3344]"
                }`}
              >
                {isUp ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                <span>
                  {isUp ? "+" : ""}
                  {idx.changePct.toFixed(2)}%
                </span>
              </span>
            </div>
          );
        })}
      </div>
      <div className="flex items-center space-x-3 text-gray-500 pl-4 border-l border-[#1f2433]">
        <button
          onClick={fetchIndices}
          className="hover:text-[#ff9900] transition-colors p-1"
          title="Refresh Ticker Tape"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>
    </div>
  );
}
