"use client"

import * as React from "react"
import { Button } from "components/ui/button"
import { ChevronRight } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "components/ui/dropdown-menu"

// Import drawing logic
import { TrendLine, Ray, ExtendedLine, TrendAngle, HorizontalLine, VerticalLine, CrossLine } from '../drawing-logic-tsx/lines'
import { Pitchfork, SchiffPitchfork } from '../drawing-logic-tsx/pitchfork'
import { ParallelChannel, FlatTopBottomChannel, DisjointedChannel } from '../drawing-logic-tsx/channels'
import { drawCyclicLines, drawTimeCycles, drawSineLine } from '../drawing-logic-tsx/cycles'
import { GannBox, GannSquareFixed, GannFan } from '../drawing-logic-tsx/gann'
import { drawElliotImpulseWave, drawElliotCorrectionWave, drawElliotTriangleWave } from '../drawing-logic-tsx/elliot-wave'
import { ArrowMarker, Arrow, ArrowMarkUp, ArrowMarkDown } from '../drawing-logic-tsx/arrows'
import { Brush, Highlighter } from '../drawing-logic-tsx/brushes'
import { rectangle, rotatedRectangle, ellipse } from '../drawing-logic-tsx/shapes'
import { calculateLongPosition, calculateShortPosition, calculateForecast } from '../drawing-logic-tsx/projection'
import { calculatePriceRange, calculateDataRange, calculateDataPriceRange } from '../drawing-logic-tsx/measurer'

interface ToolButtonProps {
  icon: React.ReactNode
  isActive?: boolean
  dropdownItems?: React.ReactNode[]
  onSelect?: (tool: string, toolType?: string) => void
  toolType?: string
}

function ToolButton({ icon, isActive, dropdownItems, onSelect, toolType }: ToolButtonProps) {
  if (!dropdownItems?.length) {
    return (
      <Button 
        variant="ghost" 
        size="icon" 
        className={`w-full relative group ${isActive ? 'text-blue-500' : 'text-[#666]'} hover:text-white hover:bg-[#2a2a2a]`}
        onClick={() => onSelect?.('select')}
      >
        {icon}
      </Button>
    )
  }

  return (
    <div className="relative group">
      <Button 
        variant="ghost" 
        size="icon" 
        className={`w-full relative group ${isActive ? 'text-blue-500' : 'text-[#666]'} hover:text-white hover:bg-[#2a2a2a]`}
      >
        {icon}
        <ChevronRight className="h-3 w-3 absolute right-1 opacity-0 group-hover:opacity-100 transition-opacity" />
      </Button>
      <div className="absolute top-full left-0 mt-1 min-w-[180px] bg-[#1a1a1a] border-[#2a2a2a] text-white z-10 hidden group-hover:block">
        {dropdownItems.map((item, index) => (
          <React.Fragment key={index}>
            {React.isValidElement(item) ? (
              item
            ) : (
              <Button
                variant="ghost"
                className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1"
                onClick={() => onSelect?.(item.toString(), toolType)}
              >
                {item}
              </Button>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  )
}

interface DrawingToolsProps {
  onToolSelect?: (tool: string, toolType?: string) => void;
  activeTool?: string | null;
  activeToolType?: string | null;
}

export function DrawingTools({ onToolSelect, activeTool }: DrawingToolsProps) {
  return (
    <div className="w-12 bg-[#1a1a1a] border-r border-[#2a2a2a] flex flex-col py-2">
      <div className="space-y-1">
        <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M12 12L22 22M12 12L2 22M12 12L22 2M12 12L2 2" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={[
            <div key="lines-title" className="px-2 py-1 text-xs text-gray-400">LINES</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('trendLine', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2" strokeWidth="1.5" /></svg>Trend Line</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('ray', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12" strokeWidth="1.5" /></svg>Ray</React.Fragment>
            </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('infoLine', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Info Line</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('extendedLine', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 2L2 22" strokeWidth="1.5" /></svg>Extended Line</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('trendAngle', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M12 2L22 12" strokeWidth="1.5" /></svg>Trend Angle</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('horizontalLine', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12" strokeWidth="1.5" /></svg>Horizontal Line</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('horizontalRay', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 12L2 12" strokeWidth="1.5" /></svg>Horizontal Ray</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('verticalLine', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M12 2L12 22" strokeWidth="1.5" /></svg>Vertical Line</React.Fragment>
            </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('crossLine', 'lines')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Cross Line</React.Fragment>
            </Button>,
            <div key="channels-title" className="px-2 py-1 text-xs text-gray-400">CHANNELS</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('parallelChannel', 'channels')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16" strokeWidth="1.5" /></svg>Parallel Channel</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('regressionTrend', 'channels')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M4 18L20 6" strokeWidth="1.5" /></svg>Regression Trend</React.Fragment>
            </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('flatTopBottom', 'channels')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16M2 12L22 12" strokeWidth="1.5" /></svg>Flat Top/Bottom</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('disjointChannel', 'channels')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16M2 4L22 4M2 20L22 20" strokeWidth="1.5" /></svg>Disjoint Channel</React.Fragment>
            </Button>,
             <div key="pitchforks-title" className="px-2 py-1 text-xs text-gray-400">PITCHFORKS</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('pitchfork', 'pitchforks')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M12 2L12 22" strokeWidth="1.5" /></svg>Pitchfork</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('schiffPitchfork', 'pitchforks')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M7 12L17 12" strokeWidth="1.5" /></svg>Schiff Pitchfork</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('modifiedSchiffPitchfork', 'pitchforks')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M5 10L19 10" strokeWidth="1.5" /></svg>Modified Schiff Pitchfork</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('insidePitchfork', 'pitchforks')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M9 14L15 14" strokeWidth="1.5" /></svg>Inside Pitchfork</React.Fragment>
            </Button>,
          ]}
          onSelect={onToolSelect}
          toolType="lines"
        />
        <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M3 12L21 12M3 8L21 8M3 16L21 16" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={[
            <div key="fibonacci-title" className="px-2 py-1 text-xs text-gray-400">FIBONACCI</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibRetracement', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2" strokeWidth="1.5" /></svg>Fib Retracement</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('trendBasedFibExtension', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Trend-Based Fib Extension</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibChannel', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16" strokeWidth="1.5" /></svg>Fib Channel</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibTimeZone', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 2L22 22" strokeWidth="1.5" /></svg>Fib Time Zone</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibSpeedResistanceFan', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>Fib Speed Resistance Fan</React.Fragment>
            </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('trendBasedFibTime', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 18L22 6" strokeWidth="1.5" /></svg>Trend-Based Fib Time</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibCircles', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><circle cx="12" cy="12" r="8" strokeWidth="1.5" /></svg>Fib Circles</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibSpiral', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M12 2a10 10 0 0 1 0 20a10 10 0 0 1 0-20z" strokeWidth="1.5" /></svg>Fib Spiral</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibSpeedResistanceArcs', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6" strokeWidth="1.5" /></svg>Fib Speed Resistance Arcs</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('fibWedge', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M7 12L17 12" strokeWidth="1.5" /></svg>Fib Wedge</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('pitchfan', 'fibonacci')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M5 10L19 10" strokeWidth="1.5" /></svg>Pitchfan</React.Fragment>
            </Button>,
            <div key="gann-title" className="px-2 py-1 text-xs text-gray-400">GANN</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('gannBox', 'gann')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6z" strokeWidth="1.5" /></svg>Gann Box</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('gannSquareFixed', 'gann')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6zM2 12h20M12 2v20" strokeWidth="1.5" /></svg>Gann Square Fixed</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('gannSquare', 'gann')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6zM2 12h20M12 2v20M6 2h12M6 22h12" strokeWidth="1.5" /></svg>Gann Square</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('gannFan', 'gann')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M5 10L19 10" strokeWidth="1.5" /></svg>Gann Fan</React.Fragment>
            </Button>,
          ]}
          onSelect={onToolSelect}
          toolType="fibonacci"
        />
         <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M4 7h16M4 12h16M4 17h10" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={[
            <div key="patterns-title" className="px-2 py-1 text-xs text-gray-400">PATTERNS</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('xabcdPattern', 'patterns')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2" strokeWidth="1.5" /></svg>XABCD Pattern</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('cypherPattern', 'patterns')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M7 12L17 12" strokeWidth="1.5" /></svg>Cypher Pattern</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('headAndShoulders', 'patterns')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Head and Shoulders</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('abcdPattern', 'patterns')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>ABCD Pattern</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('trianglePattern', 'patterns')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6" strokeWidth="1.5" /></svg>Triangle Pattern</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('threeDrivesPattern', 'patterns')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14" strokeWidth="1.5" /></svg>Three Drives Pattern</React.Fragment>
            </Button>,
            <div key="elliott-waves-title" className="px-2 py-1 text-xs text-gray-400">ELLIOTT WAVES</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('elliottImpulseWave', 'elliottWaves')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10" strokeWidth="1.5" /></svg>Elliott Impulse Wave (12345)</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('elliottCorrectionWave', 'elliottWaves')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16" strokeWidth="1.5" /></svg>Elliott Correction Wave (ABC)</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('elliottTriangleWave', 'elliottWaves')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16M2 16L22 8" strokeWidth="1.5" /></svg>Elliott Triangle Wave (ABCDE)</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('elliottDoubleComboWave', 'elliottWaves')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16M2 16L22 8M2 4L22 20" strokeWidth="1.5" /></svg>Elliott Double Combo Wave (WXY)</React.Fragment>
            </Button>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('elliottTripleComboWave', 'elliottWaves')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16M2 16L22 8M2 4L22 20M2 20L22 4" strokeWidth="1.5" /></svg>Elliott Triple Combo Wave (WXYXZ)</React.Fragment>
            </Button>,
            <div key="cycles-title" className="px-2 py-1 text-xs text-gray-400">CYCLES</div>,
            <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('cyclicLines', 'cycles')}>
              <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Cyclic Lines</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('timeCycles', 'cycles')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Time Cycles</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('sineLine', 'cycles')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12c3 4 6 4 9 0s6-4 9 0" strokeWidth="1.5" /></svg>Sine Line</React.Fragment>
             </Button>,
           ]}
           onSelect={onToolSelect}
           toolType="patterns"
         />
         <ToolButton
           icon={
             <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
               <path d="M12 2L2 22M22 22L12 2" strokeWidth="1.5" />
             </svg>
           }
           dropdownItems={[
             <div key="arrows-title" className="px-2 py-1 text-xs text-gray-400">ARROWS</div>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('arrowMarker', 'arrows')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M12 2L12 22" strokeWidth="1.5" /></svg>Arrow Marker</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('arrow', 'arrows')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 12L12 2M22 12L12 22" strokeWidth="1.5" /></svg>Arrow</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('arrowMarkUp', 'arrows')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M12 2L12 12" strokeWidth="1.5" /></svg>Arrow Mark Up</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('arrowMarkDown', 'arrows')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M12 22L12 12" strokeWidth="1.5" /></svg>Arrow Mark Down</React.Fragment>
             </Button>,
           ]}
           onSelect={onToolSelect}
           toolType="arrows"
         />
         <ToolButton
           icon={
             <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
               <path d="M2 2h20v20H2z" strokeWidth="1.5" />
             </svg>
           }
           dropdownItems={[
             <div key="shapes-title" className="px-2 py-1 text-xs text-gray-400">SHAPES</div>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('rectangle', 'shapes')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2z" strokeWidth="1.5" /></svg>Rectangle</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('rotatedRectangle', 'shapes')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6z" strokeWidth="1.5" /></svg>Rotated Rectangle</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('ellipse', 'shapes')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><circle cx="12" cy="12" r="10" strokeWidth="1.5" /></svg>Ellipse</React.Fragment>
             </Button>,
           ]}
           onSelect={onToolSelect}
           toolType="shapes"
         />
         <ToolButton
           icon={
             <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
               <path d="M2 12L22 12M2 8L22 8M2 16L22 16" strokeWidth="1.5" />
             </svg>
           }
           dropdownItems={[
             <div key="brushes-title" className="px-2 py-1 text-xs text-gray-400">BRUSHES</div>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('brush', 'brushes')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Brush</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('highlighter', 'brushes')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Highlighter</React.Fragment>
             </Button>,
           ]}
           onSelect={onToolSelect}
           toolType="brushes"
         />
         <ToolButton
           icon={
             <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
               <path d="M2 12L22 12M2 8L22 8M2 16L22 16" strokeWidth="1.5" />
             </svg>
           }
           dropdownItems={[
             <div key="projection-title" className="px-2 py-1 text-xs text-gray-400">PROJECTION</div>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('longPosition', 'projection')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Long Position</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('shortPosition', 'projection')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Short Position</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('forecast', 'projection')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>Forecast</React.Fragment>
             </Button>,
           ]}
           onSelect={onToolSelect}
           toolType="projection"
         />
         <ToolButton
           icon={
             <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
               <path d="M2 12L22 12M2 8L22 8M2 16L22 16" strokeWidth="1.5" />
             </svg>
           }
           dropdownItems={[
             <div key="measurer-title" className="px-2 py-1 text-xs text-gray-400">MEASURER</div>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('priceRange', 'measurer')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Price Range</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('dataRange', 'measurer')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Data Range</React.Fragment>
             </Button>,
             <Button variant="ghost" className="w-full text-left hover:bg-[#2a2a2a] px-2 py-1" onClick={() => onToolSelect?.('dataPriceRange', 'measurer')}>
               <React.Fragment><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>Data & Price Range</React.Fragment>
             </Button>,
           ]}
           onSelect={onToolSelect}
           toolType="measurer"
         />
       </div>
     </div>
     )
    }
