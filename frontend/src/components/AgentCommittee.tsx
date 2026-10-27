"use client";

import React, { useState } from "react";
import {
  ShieldAlert,
  BrainCircuit,
  BarChart3,
  TrendingUp,
  Newspaper,
  CheckCircle2,
  AlertTriangle,
  Award,
  Target,
  Percent
} from "lucide-react";

interface AgentResult {
  agent: string;
  score: number;
  verdict: string;
  pros?: string[];
  cons?: string[];
  report: string;
  intrinsicValue?: number;
  upside?: number;
  rsi?: number;
  riskGrade?: string;
  suggestedStopLoss?: number;
  portfolioAllocation?: string;
  bullishArticles?: number;
  bearishArticles?: number;
  headlines?: Array<{ title: string; sentiment: string; publisher: string }>;
}

interface CommitteeData {
  cio: {
    compositeScore: number;
    recommendation: string;
    actionColor: string;
    targetPrice: number;
    expectedReturn: number;
    executiveSummary: string;
    agentScores: {
      fundamental: number;
      technical: number;
      sentiment: number;
      risk: number;
    };
  };
  fundamental: AgentResult;
  technical: AgentResult;
  sentiment: AgentResult;
  risk: AgentResult;
}

interface AgentCommitteeProps {
  committee: CommitteeData;
}

export default function AgentCommittee({ committee }: AgentCommitteeProps) {
  const [activeTab, setActiveTab] = useState<"all" | "fundamental" | "technical" | "sentiment" | "risk">("all");

  const { cio, fundamental, technical, sentiment, risk } = committee;

  return (
    <div className="space-y-4">
      {/* 👑 CIO Lead Analyst Verdict Header Banner */}
      <div className="bg-[#121520] border-2 border-[#ff9900]/40 rounded-lg p-5 shadow-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-[#ff9900]/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[#22283a]">
          <div className="flex items-start space-x-3">
            <div className="p-2.5 rounded-lg bg-[#ff9900]/20 border border-[#ff9900]/40 text-[#ff9900]">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-semibold text-[#ff9900] tracking-wider uppercase">
                  INVESTMENT COMMITTEE EXECUTIVE DECISION
                </span>
                <span className="text-[10px] bg-white/10 text-gray-300 px-1.5 py-0.5 rounded font-mono">
                  AUTONOMOUS AGENTS
                </span>
              </div>
              <h2 className="text-2xl font-black tracking-tight flex items-center space-x-3 mt-1">
                <span style={{ color: cio.actionColor }}>{cio.recommendation}</span>
                <span className="text-sm font-normal text-gray-400 font-mono">
                  (Composite Score: <strong className="text-white text-base">{cio.compositeScore}</strong>/100)
                </span>
              </h2>
            </div>
          </div>

          {/* Target Price & Expected Return Box */}
          <div className="flex items-center space-x-4 bg-[#0a0c12] border border-[#23293d] px-4 py-2.5 rounded-lg">
            <div>
              <div className="text-[10px] font-mono text-gray-400 flex items-center space-x-1">
                <Target className="w-3 h-3 text-[#ff9900]" />
                <span>12M TARGET PRICE</span>
              </div>
              <div className="text-xl font-bold font-mono text-white mt-0.5">
                ${cio.targetPrice}
              </div>
            </div>
            <div className="h-8 w-px bg-[#23293d]" />
            <div>
              <div className="text-[10px] font-mono text-gray-400 flex items-center space-x-1">
                <Percent className="w-3 h-3 text-[#00ff66]" />
                <span>EXP. RETURN</span>
              </div>
              <div
                className={`text-xl font-bold font-mono mt-0.5 ${
                  cio.expectedReturn >= 0 ? "text-[#00ff66]" : "text-[#ff3344]"
                }`}
              >
                {cio.expectedReturn >= 0 ? "+" : ""}
                {cio.expectedReturn}%
              </div>
            </div>
          </div>
        </div>

        {/* Executive Summary Memo */}
        <div className="mt-4 bg-[#0a0c12]/80 border border-[#1d2232] rounded p-3.5 text-xs font-mono leading-relaxed text-gray-300 whitespace-pre-line">
          {cio.executiveSummary}
        </div>

        {/* 4 Agent Score Meters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 pt-3 border-t border-[#1d2232]">
          {[
            { name: "FUNDAMENTAL", score: cio.agentScores.fundamental, icon: BarChart3, color: "#38bdf8" },
            { name: "TECHNICAL", score: cio.agentScores.technical, icon: TrendingUp, color: "#a855f7" },
            { name: "SENTIMENT", score: cio.agentScores.sentiment, icon: Newspaper, color: "#f59e0b" },
            { name: "RISK / MDD", score: cio.agentScores.risk, icon: ShieldAlert, color: "#10b981" },
          ].map((item) => (
            <div key={item.name} className="bg-[#0b0d14] p-2.5 rounded border border-[#1b2030]">
              <div className="flex items-center justify-between text-[11px] font-mono text-gray-400">
                <span className="flex items-center space-x-1">
                  <item.icon className="w-3 h-3" style={{ color: item.color }} />
                  <span>{item.name}</span>
                </span>
                <span className="font-bold text-white">{item.score}</span>
              </div>
              <div className="w-full bg-[#1b2030] h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${item.score}%`,
                    backgroundColor: item.color,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tabs for Detailed Agent Insights */}
      <div className="flex items-center space-x-2 border-b border-[#212638] pb-2 text-xs font-mono">
        <button
          onClick={() => setActiveTab("all")}
          className={`px-3 py-1.5 rounded transition-colors ${
            activeTab === "all" ? "bg-[#ff9900] text-black font-bold" : "text-gray-400 hover:text-white"
          }`}
        >
          ALL AGENTS (4)
        </button>
        <button
          onClick={() => setActiveTab("fundamental")}
          className={`px-3 py-1.5 rounded transition-colors ${
            activeTab === "fundamental" ? "bg-[#38bdf8] text-black font-bold" : "text-gray-400 hover:text-white"
          }`}
        >
          FUNDAMENTAL
        </button>
        <button
          onClick={() => setActiveTab("technical")}
          className={`px-3 py-1.5 rounded transition-colors ${
            activeTab === "technical" ? "bg-[#a855f7] text-white font-bold" : "text-gray-400 hover:text-white"
          }`}
        >
          TECHNICAL
        </button>
        <button
          onClick={() => setActiveTab("sentiment")}
          className={`px-3 py-1.5 rounded transition-colors ${
            activeTab === "sentiment" ? "bg-[#f59e0b] text-black font-bold" : "text-gray-400 hover:text-white"
          }`}
        >
          NEWS & SENTIMENT
        </button>
        <button
          onClick={() => setActiveTab("risk")}
          className={`px-3 py-1.5 rounded transition-colors ${
            activeTab === "risk" ? "bg-[#10b981] text-black font-bold" : "text-gray-400 hover:text-white"
          }`}
        >
          RISK & ALLOCATION
        </button>
      </div>

      {/* Agents Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 1. Fundamental Agent Card */}
        {(activeTab === "all" || activeTab === "fundamental") && (
          <div className="bg-[#0f121a] border border-[#202538] rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-[#1b2030] pb-2">
              <div className="flex items-center space-x-2">
                <BarChart3 className="w-4 h-4 text-[#38bdf8]" />
                <h3 className="text-sm font-bold font-mono text-white">FUNDAMENTAL AGENT</h3>
              </div>
              <span className="text-xs font-mono font-bold text-[#38bdf8] px-2 py-0.5 rounded bg-[#38bdf8]/10 border border-[#38bdf8]/30">
                SCORE: {fundamental.score}/100
              </span>
            </div>

            <div className="text-xs font-mono text-gray-300 font-semibold">
              VERDICT: <span className="text-white">{fundamental.verdict}</span>
            </div>

            <div className="space-y-1.5 text-xs font-mono">
              {fundamental.pros?.map((p, i) => (
                <div key={i} className="flex items-start space-x-2 text-[#00ff66]">
                  <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{p}</span>
                </div>
              ))}
              {fundamental.cons?.map((c, i) => (
                <div key={i} className="flex items-start space-x-2 text-[#ff9900]">
                  <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{c}</span>
                </div>
              ))}
            </div>

            <div className="bg-[#090b10] p-2.5 rounded border border-[#1b2030] text-[11px] font-mono text-gray-400 leading-relaxed">
              {fundamental.report}
            </div>
          </div>
        )}

        {/* 2. Technical Agent Card */}
        {(activeTab === "all" || activeTab === "technical") && (
          <div className="bg-[#0f121a] border border-[#202538] rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-[#1b2030] pb-2">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-[#a855f7]" />
                <h3 className="text-sm font-bold font-mono text-white">TECHNICAL AGENT</h3>
              </div>
              <span className="text-xs font-mono font-bold text-[#a855f7] px-2 py-0.5 rounded bg-[#a855f7]/10 border border-[#a855f7]/30">
                SCORE: {technical.score}/100
              </span>
            </div>

            <div className="text-xs font-mono text-gray-300 font-semibold">
              VERDICT: <span className="text-white">{technical.verdict}</span>
            </div>

            <div className="space-y-1.5 text-xs font-mono">
              {technical.pros?.map((p, i) => (
                <div key={i} className="flex items-start space-x-2 text-[#00ff66]">
                  <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{p}</span>
                </div>
              ))}
              {technical.cons?.map((c, i) => (
                <div key={i} className="flex items-start space-x-2 text-[#ff9900]">
                  <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{c}</span>
                </div>
              ))}
            </div>

            <div className="bg-[#090b10] p-2.5 rounded border border-[#1b2030] text-[11px] font-mono text-gray-400 leading-relaxed">
              {technical.report}
            </div>
          </div>
        )}

        {/* 3. Sentiment & News Agent Card */}
        {(activeTab === "all" || activeTab === "sentiment") && (
          <div className="bg-[#0f121a] border border-[#202538] rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-[#1b2030] pb-2">
              <div className="flex items-center space-x-2">
                <Newspaper className="w-4 h-4 text-[#f59e0b]" />
                <h3 className="text-sm font-bold font-mono text-white">NEWS & SENTIMENT AGENT</h3>
              </div>
              <span className="text-xs font-mono font-bold text-[#f59e0b] px-2 py-0.5 rounded bg-[#f59e0b]/10 border border-[#f59e0b]/30">
                SCORE: {sentiment.score}/100
              </span>
            </div>

            <div className="text-xs font-mono text-gray-300 font-semibold">
              VERDICT: <span className="text-white">{sentiment.verdict}</span>
            </div>

            <div className="space-y-1.5 text-xs font-mono">
              {sentiment.pros?.map((p, i) => (
                <div key={i} className="flex items-start space-x-2 text-[#00ff66]">
                  <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{p}</span>
                </div>
              ))}
              {sentiment.cons?.map((c, i) => (
                <div key={i} className="flex items-start space-x-2 text-[#ff9900]">
                  <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{c}</span>
                </div>
              ))}
            </div>

            <div className="bg-[#090b10] p-2.5 rounded border border-[#1b2030] text-[11px] font-mono text-gray-400 leading-relaxed">
              {sentiment.report}
            </div>
          </div>
        )}

        {/* 4. Risk Manager Agent Card */}
        {(activeTab === "all" || activeTab === "risk") && (
          <div className="bg-[#0f121a] border border-[#202538] rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-[#1b2030] pb-2">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="w-4 h-4 text-[#10b981]" />
                <h3 className="text-sm font-bold font-mono text-white">RISK MANAGER AGENT</h3>
              </div>
              <span className="text-xs font-mono font-bold text-[#10b981] px-2 py-0.5 rounded bg-[#10b981]/10 border border-[#10b981]/30">
                SCORE: {risk.score}/100
              </span>
            </div>

            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-gray-400">RISK GRADE:</span>
              <strong className="text-white">{risk.riskGrade}</strong>
            </div>

            <div className="flex items-center justify-between text-xs font-mono bg-[#0b0e15] p-2 rounded border border-[#1f2538]">
              <span className="text-gray-400">STOP-LOSS LEVEL:</span>
              <strong className="text-[#ff3344]">${risk.suggestedStopLoss}</strong>
            </div>

            <div className="flex items-center justify-between text-xs font-mono bg-[#0b0e15] p-2 rounded border border-[#1f2538]">
              <span className="text-gray-400">RECOMMENDED ALLOCATION:</span>
              <strong className="text-[#00ff66]">{risk.portfolioAllocation}</strong>
            </div>

            <div className="bg-[#090b10] p-2.5 rounded border border-[#1b2030] text-[11px] font-mono text-gray-400 leading-relaxed">
              {risk.report}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
