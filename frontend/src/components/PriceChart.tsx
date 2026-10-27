"use client";

import React, { useState, useMemo } from "react";
import { Maximize2, Activity } from "lucide-react";

interface BarData {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface PriceChartProps {
  symbol: string;
  chartData: BarData[];
  onPeriodChange: (period: string) => void;
  currentPeriod: string;
}

export default function PriceChart({
  symbol,
  chartData,
  onPeriodChange,
  currentPeriod,
}: PriceChartProps) {
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);
  const [chartType, setChartType] = useState<"area" | "candle">("area");

  const { minPrice, maxPrice, maxVolume } = useMemo(() => {
    if (!chartData || chartData.length === 0) {
      return { minPrice: 0, maxPrice: 100, maxVolume: 1000 };
    }
    let min = Infinity;
    let max = -Infinity;
    let maxVol = 0;
    for (const b of chartData) {
      if (b.low < min) min = b.low;
      if (b.high > max) max = b.high;
      if (b.volume > maxVol) maxVol = b.volume;
    }
    const padding = (max - min) * 0.05 || 1;
    return {
      minPrice: Math.max(0, min - padding),
      maxPrice: max + padding,
      maxVolume: maxVol,
    };
  }, [chartData]);

  const activeBar = hoverIndex !== null && chartData[hoverIndex] ? chartData[hoverIndex] : chartData[chartData.length - 1];

  // SVG dimensions
  const width = 800;
  const height = 340;
  const chartHeight = 260;
  const volumeHeight = 60;
  const priceRange = maxPrice - minPrice || 1;

  const points = useMemo(() => {
    if (!chartData || chartData.length === 0) return "";
    return chartData
      .map((d, i) => {
        const x = (i / (chartData.length - 1)) * width;
        const y = chartHeight - ((d.close - minPrice) / priceRange) * chartHeight;
        return `${x},${y}`;
      })
      .join(" ");
  }, [chartData, minPrice, priceRange, chartHeight, width]);

  const areaD = useMemo(() => {
    if (!points) return "";
    return `M 0,${chartHeight} L ${points} L ${width},${chartHeight} Z`;
  }, [points, chartHeight, width]);

  return (
    <div className="bg-[#0f1118] border border-[#1e2333] rounded-lg p-4 flex flex-col h-full">
      {/* Chart Header Bar */}
      <div className="flex flex-wrap items-center justify-between pb-3 mb-2 border-b border-[#1b1f2e] gap-2">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5 bg-[#ff9900]/10 border border-[#ff9900]/30 px-2 py-0.5 rounded text-xs font-mono text-[#ff9900]">
            <Activity className="w-3.5 h-3.5" />
            <span className="font-bold">{symbol} TECHNICAL CHART</span>
          </div>

          {activeBar && (
            <div className="hidden sm:flex items-center space-x-3 text-xs font-mono text-gray-400">
              <span>DATE: <strong className="text-white">{activeBar.time}</strong></span>
              <span>O: <strong className="text-white">${activeBar.open}</strong></span>
              <span>H: <strong className="text-white">${activeBar.high}</strong></span>
              <span>L: <strong className="text-white">${activeBar.low}</strong></span>
              <span>C: <strong className="text-[#ff9900]">${activeBar.close}</strong></span>
              <span>VOL: <strong className="text-gray-300">{(activeBar.volume / 1e6).toFixed(1)}M</strong></span>
            </div>
          )}
        </div>

        {/* Controls: Chart Type & Period */}
        <div className="flex items-center space-x-2 text-xs font-mono">
          <div className="flex rounded border border-[#262c3f] overflow-hidden">
            <button
              onClick={() => setChartType("area")}
              className={`px-2 py-0.5 transition-colors ${
                chartType === "area" ? "bg-[#ff9900] text-black font-bold" : "text-gray-400 hover:text-white"
              }`}
            >
              LINE
            </button>
            <button
              onClick={() => setChartType("candle")}
              className={`px-2 py-0.5 transition-colors ${
                chartType === "candle" ? "bg-[#ff9900] text-black font-bold" : "text-gray-400 hover:text-white"
              }`}
            >
              CANDLE
            </button>
          </div>

          <div className="flex rounded border border-[#262c3f] overflow-hidden">
            {["1mo", "3mo", "6mo", "1y"].map((p) => (
              <button
                key={p}
                onClick={() => onPeriodChange(p)}
                className={`px-2 py-0.5 uppercase transition-colors ${
                  currentPeriod === p
                    ? "bg-[#1e2436] text-[#ff9900] font-bold border-b-2 border-[#ff9900]"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* SVG Interactive Canvas */}
      <div
        className="relative flex-1 min-h-[300px] w-full cursor-crosshair select-none"
        onMouseMove={(e) => {
          const rect = e.currentTarget.getBoundingClientRect();
          const mouseX = e.clientX - rect.left;
          const ratio = Math.max(0, Math.min(1, mouseX / rect.width));
          const idx = Math.round(ratio * (chartData.length - 1));
          setHoverIndex(idx);
        }}
        onMouseLeave={() => setHoverIndex(null)}
      >
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-full overflow-visible"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ff9900" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#ff9900" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          {[0.2, 0.4, 0.6, 0.8].map((ratio) => (
            <line
              key={ratio}
              x1="0"
              y1={chartHeight * ratio}
              x2={width}
              y2={chartHeight * ratio}
              stroke="#1a1e2d"
              strokeDasharray="4 4"
            />
          ))}

          {/* Volume separator */}
          <line x1="0" y1={chartHeight + 10} x2={width} y2={chartHeight + 10} stroke="#22283a" />

          {/* Volume bars */}
          {chartData.map((d, i) => {
            const x = (i / (chartData.length - 1 || 1)) * width;
            const barW = Math.max(2, width / chartData.length - 1.5);
            const vHeight = maxVolume > 0 ? (d.volume / maxVolume) * volumeHeight : 0;
            const y = height - vHeight;
            const isUp = d.close >= d.open;
            return (
              <rect
                key={`vol-${i}`}
                x={x - barW / 2}
                y={y}
                width={barW}
                height={vHeight}
                fill={isUp ? "#00ff66" : "#ff3344"}
                opacity={0.35}
              />
            );
          })}

          {chartType === "area" ? (
            <>
              {/* Gradient Area */}
              <path d={areaD} fill="url(#areaGrad)" />
              {/* Stroke Line */}
              <polyline
                fill="none"
                stroke="#ff9900"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={points}
              />
            </>
          ) : (
            /* Candlestick view */
            chartData.map((d, i) => {
              const x = (i / (chartData.length - 1 || 1)) * width;
              const barW = Math.max(2.5, width / chartData.length - 2);
              const yOpen = chartHeight - ((d.open - minPrice) / priceRange) * chartHeight;
              const yClose = chartHeight - ((d.close - minPrice) / priceRange) * chartHeight;
              const yHigh = chartHeight - ((d.high - minPrice) / priceRange) * chartHeight;
              const yLow = chartHeight - ((d.low - minPrice) / priceRange) * chartHeight;
              const isUp = d.close >= d.open;
              const color = isUp ? "#00ff66" : "#ff3344";

              return (
                <g key={`candle-${i}`}>
                  {/* High/Low Wick */}
                  <line x1={x} y1={yHigh} x2={x} y2={yLow} stroke={color} strokeWidth="1.2" />
                  {/* Body */}
                  <rect
                    x={x - barW / 2}
                    y={Math.min(yOpen, yClose)}
                    width={barW}
                    height={Math.max(1.5, Math.abs(yClose - yOpen))}
                    fill={color}
                  />
                </g>
              );
            })
          )}

          {/* Hover Crosshair & Indicator Point */}
          {hoverIndex !== null && chartData[hoverIndex] && (
            <>
              <line
                x1={(hoverIndex / (chartData.length - 1)) * width}
                y1={0}
                x2={(hoverIndex / (chartData.length - 1)) * width}
                y2={height}
                stroke="#ff9900"
                strokeDasharray="3 3"
                strokeWidth="1"
              />
              <circle
                cx={(hoverIndex / (chartData.length - 1)) * width}
                cy={chartHeight - ((chartData[hoverIndex].close - minPrice) / priceRange) * chartHeight}
                r="4.5"
                fill="#ff9900"
                stroke="#000"
                strokeWidth="2"
              />
            </>
          )}
        </svg>

        {/* Y-axis price labels on the right edge */}
        <div className="absolute right-1 top-2 bottom-16 flex flex-col justify-between text-[10px] font-mono text-gray-500 pointer-events-none">
          <span>${maxPrice.toFixed(1)}</span>
          <span>${((maxPrice + minPrice) / 2).toFixed(1)}</span>
          <span>${minPrice.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
}
