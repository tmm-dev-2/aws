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
}

function ToolButton({ icon, isActive, dropdownItems }: ToolButtonProps) {
  if (!dropdownItems?.length) {
    return (
      <Button 
        variant="ghost" 
        size="icon" 
        className={`w-full relative group ${isActive ? 'text-blue-500' : 'text-[#666]'} hover:text-white hover:bg-[#2a2a2a]`}
      >
        {icon}
      </Button>
    )
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button 
          variant="ghost" 
          size="icon" 
          className={`w-full relative group ${isActive ? 'text-blue-500' : 'text-[#666]'} hover:text-white hover:bg-[#2a2a2a]`}
        >
          {icon}
          <ChevronRight className="h-3 w-3 absolute right-1 opacity-0 group-hover:opacity-100 transition-opacity" />
        </Button>
      </DropdownMenuTrigger>
        <DropdownMenuContent side="right" align="start" className="min-w-[180px] bg-[#1a1a1a] border-[#2a2a2a] text-white">
        {dropdownItems.map((item, index) => (
          <React.Fragment key={index}>
            {React.isValidElement(item) ? (
              item
            ) : (
              <DropdownMenuItem>{item}</DropdownMenuItem>
            )}
          </React.Fragment>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export function DrawingTools() {
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
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2" strokeWidth="1.5" /></svg>Trend Line</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12" strokeWidth="1.5" /></svg>Ray</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Info Line</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 2L2 22" strokeWidth="1.5" /></svg>Extended Line</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M12 2L22 12" strokeWidth="1.5" /></svg>Trend Angle</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12" strokeWidth="1.5" /></svg>Horizontal Line</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 12L2 12" strokeWidth="1.5" /></svg>Horizontal Ray</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M12 2L12 22" strokeWidth="1.5" /></svg>Vertical Line</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Cross Line</div></DropdownMenuItem>,
            <div key="channels-title" className="px-2 py-1 text-xs text-gray-400">CHANNELS</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16" strokeWidth="1.5" /></svg>Parallel Channel</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M4 18L20 6" strokeWidth="1.5" /></svg>Regression Trend</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16M2 12L22 12" strokeWidth="1.5" /></svg>Flat Top/Bottom</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16M2 4L22 4M2 20L22 20" strokeWidth="1.5" /></svg>Disjoint Channel</div></DropdownMenuItem>,
             <div key="pitchforks-title" className="px-2 py-1 text-xs text-gray-400">PITCHFORKS</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M12 2L12 22" strokeWidth="1.5" /></svg>Pitchfork</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M7 12L17 12" strokeWidth="1.5" /></svg>Schiff Pitchfork</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M5 10L19 10" strokeWidth="1.5" /></svg>Modified Schiff Pitchfork</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M9 14L15 14" strokeWidth="1.5" /></svg>Inside Pitchfork</div></DropdownMenuItem>,
          ]}
        />
        <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M3 12L21 12M3 8L21 8M3 16L21 16" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={[
            <div key="fibonacci-title" className="px-2 py-1 text-xs text-gray-400">FIBONACCI</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2" strokeWidth="1.5" /></svg>Fib Retracement</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Trend-Based Fib Extension</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 8L22 8M2 16L22 16" strokeWidth="1.5" /></svg>Fib Channel</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 2L22 22" strokeWidth="1.5" /></svg>Fib Time Zone</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>Fib Speed Resistance Fan</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 18L22 6" strokeWidth="1.5" /></svg>Trend-Based Fib Time</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><circle cx="12" cy="12" r="8" strokeWidth="1.5" /></svg>Fib Circles</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M12 2a10 10 0 0 1 0 20a10 10 0 0 1 0-20z" strokeWidth="1.5" /></svg>Fib Spiral</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6" strokeWidth="1.5" /></svg>Fib Speed Resistance Arcs</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M7 12L17 12" strokeWidth="1.5" /></svg>Fib Wedge</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M5 10L19 10" strokeWidth="1.5" /></svg>Pitchfan</div></DropdownMenuItem>,
            <div key="gann-title" className="px-2 py-1 text-xs text-gray-400">GANN</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6z" strokeWidth="1.5" /></svg>Gann Box</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6zM2 12h20M12 2v20" strokeWidth="1.5" /></svg>Gann Square Fixed</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6zM2 12h20M12 2v20M6 2h12M6 22h12" strokeWidth="1.5" /></svg>Gann Square</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M5 10L19 10" strokeWidth="1.5" /></svg>Gann Fan</div></DropdownMenuItem>,
          ]}
        />
         <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M4 7h16M4 12h16M4 17h10" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={[
            <div key="patterns-title" className="px-2 py-1 text-xs text-gray-400">PATTERNS</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2" strokeWidth="1.5" /></svg>XABCD Pattern</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M7 12L17 12" strokeWidth="1.5" /></svg>Cypher Pattern</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Head and Shoulders</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>ABCD Pattern</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6" strokeWidth="1.5" /></svg>Triangle Pattern</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14" strokeWidth="1.5" /></svg>Three Drives Pattern</div></DropdownMenuItem>,
            <div key="elliott-waves-title" className="px-2 py-1 text-xs text-gray-400">ELLIOTT WAVES</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10" strokeWidth="1.5" /></svg>Elliott Impulse Wave (12345)</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16" strokeWidth="1.5" /></svg>Elliott Correction Wave (ABC)</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16M2 16L22 8" strokeWidth="1.5" /></svg>Elliott Triangle Wave (ABCDE)</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16M2 16L22 8M2 4L22 20" strokeWidth="1.5" /></svg>Elliott Double Combo Wave (WXY)</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L12 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 10L22 14M2 14L22 10M2 8L22 16M2 16L22 8M2 4L22 20M2 20L22 4" strokeWidth="1.5" /></svg>Elliott Triple Combo Wave (WXYXZ)</div></DropdownMenuItem>,
            <div key="cycles-title" className="px-2 py-1 text-xs text-gray-400">CYCLES</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 6M2 18L22 18" strokeWidth="1.5" /></svg>Cyclic Lines</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 6M2 18L22 18M2 4L22 4M2 20L22 20" strokeWidth="1.5" /></svg>Time Cycles</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12C2 16.4183 5.58172 20 10 20C14.4183 20 18 16.4183 18 12C18 7.58172 14.4183 4 10 4C5.58172 4 2 7.58172 2 12Z" strokeWidth="1.5" /></svg>Sine Line</div></DropdownMenuItem>,
          ]}
        />
        <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M4 12h16M8 12v4" strokeWidth="1.5" />
            </svg>
          }
           dropdownItems={[
            <div key="projection-title" className="px-2 py-1 text-xs text-gray-400">PROJECTION</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>Long Position</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 18L22 6" strokeWidth="1.5" /></svg>Short Position</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18M2 18L22 6" strokeWidth="1.5" /></svg>Forecast</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18M2 18L22 6M2 4L22 20" strokeWidth="1.5" /></svg>Bars Pattern</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18M2 18L22 6M2 4L22 20M2 20L22 4" strokeWidth="1.5" /></svg>Ghost Feed</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18M2 18L22 6M2 4L22 20M2 20L22 4M2 8L22 16" strokeWidth="1.5" /></svg>Projection</div></DropdownMenuItem>,
            <div key="measurer-title" className="px-2 py-1 text-xs text-gray-400">MEASURER</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18M2 18L22 6M2 4L22 20M2 20L22 4M2 8L22 16M2 16L22 8M2 10L22 14M2 14L22 10M2 2L22 22" strokeWidth="1.5" /></svg>Price Range</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18M2 18L22 6M2 4L22 20M2 20L22 4M2 8L22 16M2 16L22 8M2 10L22 14M2 14L22 10M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Date Range</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 12L22 12M2 6L22 18M2 18L22 6M2 4L22 20M2 20L22 4M2 8L22 16M2 16L22 8M2 10L22 14M2 14L22 10M2 2L22 22M2 22L22 2M2 14L22 10" strokeWidth="1.5" /></svg>Date and Price Range</div></DropdownMenuItem>,
          ]}
        />
         
         <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <circle cx="11" cy="11" r="7" strokeWidth="1.5" />
              <path d="M16 16l4 4" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={[
            <div key="brushes-title" className="px-2 py-1 text-xs text-gray-400">BRUSHES</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2" strokeWidth="1.5" /></svg>Brush</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Highlighter</div></DropdownMenuItem>,
            <div key="arrows-title" className="px-2 py-1 text-xs text-gray-400">ARROWS</div>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12M2 6L22 18" strokeWidth="1.5" /></svg>Arrow Marker</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12M2 18L22 6" strokeWidth="1.5" /></svg>Arrow</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6" strokeWidth="1.5" /></svg>Arrow Mark Up</div></DropdownMenuItem>,
            <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12M2 6L22 18M2 18L22 6M2 4L22 20" strokeWidth="1.5" /></svg>Arrow Mark Down</div></DropdownMenuItem>,
            <div key="shapes-title" className="px-2 py-1 text-xs text-gray-400">SHAPES</div>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2z" strokeWidth="1.5" /></svg>Rectangle</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2h20v20H2zM6 6h12v12H6z" strokeWidth="1.5" /></svg>Rotated Rectangle</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 2L22 22M2 22L22 2M2 12L22 12" strokeWidth="1.5" /></svg>Path</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><circle cx="12" cy="12" r="8" strokeWidth="1.5" /></svg>Circle</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M12 2a10 10 0 0 1 0 20a10 10 0 0 1 0-20z" strokeWidth="1.5" /></svg>Ellipse</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M12 2L12 22M5 10L19 10" strokeWidth="1.5" /></svg>Polyline</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M12 2L12 22M5 10L19 10" strokeWidth="1.5" /></svg>Triangle</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M12 2L12 22M5 10L19 10" strokeWidth="1.5" /></svg>Arc</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M12 2L12 22M5 10L19 10" strokeWidth="1.5" /></svg>Curve</div></DropdownMenuItem>,
             <DropdownMenuItem><div drawing-tool="Name"><svg viewBox="0 0 24 24" className="h-3 w-3 mr-1 fill-none stroke-current"><path d="M2 22L12 2L22 22M12 2L12 22M5 10L19 10" strokeWidth="1.5" /></svg>Double Curve</div></DropdownMenuItem>,
          ]}
        />
      </div>
      <div className="mt-auto space-y-1">
        <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <circle cx="12" cy="12" r="2" strokeWidth="1.5" />
              <path d="M12 19c-4 0-7-3-7-7s3-7 7-7 7 3 7 7-3 7-7 7z" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={["Clear All", "Clear Selected", "Clear Last"]}
        />
         <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M4 6h16M4 12h16M4 18h16" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={["Show All", "Hide Selected", "Show Selected"]}
        />
        <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M12 6v12M6 12h12" strokeWidth="1.5" />
              <path d="M17 17l-5-5l5-5" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={["Magnet", "Snap to Price", "Snap to Time"]}
        />
        <ToolButton
          icon={
            <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current">
              <path d="M12 17v-6M8 7h8v4H8z" strokeWidth="1.5" />
              <path d="M6 17h12" strokeWidth="1.5" />
            </svg>
          }
          dropdownItems={["Lock All", "Lock Selected", "Unlock All"]}
        />
      </div>
    </div>
  )
}

             
