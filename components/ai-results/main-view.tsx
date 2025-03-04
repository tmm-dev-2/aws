"use client"

import { useEffect, useRef } from 'react'
import { createChart,  LineStyle } from 'lightweight-charts'

interface PatternData {
  coordinates: number[][]
  ohlcv: {
    open: number[]
    high: number[]
    low: number[]
    close: number[]
    volume: number[]
  }
  dates: string[]
  analysis: string
  prediction: string
  confidence: number
}

interface MainViewProps {
  patternId: string
  patternData?: PatternData
}

export const MainView = ({ patternId, patternData }: MainViewProps) => {
  const chartRef = useRef<HTMLDivElement>(null)

    
  useEffect(() => {
    if (!chartRef.current || !patternData) return

    const chart = createChart(chartRef.current, {
      width: chartRef.current.clientWidth,
      height: 400,
      layout: {
        background: { color: '#1A1A1A' },
        textColor: '#d1d4dc',
        fontSize: 12,
        fontFamily: 'Inter, sans-serif'
      },
      grid: {
        vertLines: { color: '#2a2e39' },
        horzLines: { color: '#2a2e39' },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: {
          color: '#2962FF',
          width: 1,
          style: LineStyle.Dotted,
        },
        horzLine: {
          color: '#2962FF',
          width: 1,
          style: LineStyle.Dotted,
        },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    })

    

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350'
    })

    // Format OHLCV data for the chart
    const candleData = patternData.dates.map((date, i) => ({
      time: new Date(date).getTime() / 1000,
      open: patternData.ohlcv.open[i],
      high: patternData.ohlcv.high[i],
      low: patternData.ohlcv.low[i],
      close: patternData.ohlcv.close[i]
    }))

    candlestickSeries.setData(candleData)

    // Add markers for pattern occurrences
    const markers = patternData.coordinates.map(coord => ({
      time: new Date(patternData.dates[coord[0]]).getTime() / 1000,
      position: 'belowBar',
      color: '#2196F3',
      shape: 'arrowUp',
      text: patternId.replace('_', ' ').toUpperCase()
    }))

    candlestickSeries.setMarkers(markers)

    const handleResize = () => {
      chart.applyOptions({
        width: chartRef.current?.clientWidth || 600
      })
    }

    window.addEventListener('resize', handleResize)

    return () => {
      chart.remove()
      window.removeEventListener('resize', handleResize)
    }
  }, [patternId, patternData])

  if (!patternData) {
    return <div className="flex-1 p-6">Select a pattern to view analysis</div>
  }

  return (
    <div className="flex-1 p-6 overflow-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">
          {patternId.replace('_', ' ').toUpperCase()}
        </h2>
        <div className="bg-[#2a2e39] rounded-lg p-4 mb-4">
          <h3 className="text-xl font-semibold mb-2">Pattern Analysis</h3>
          <p className="text-gray-300">{patternData.analysis}</p>
        </div>
      </div>

      <div className="bg-[#2a2e39] rounded-lg p-4 mb-6">
        <div ref={chartRef} className="mb-4" />
      </div>

      <div className="bg-[#2a2e39] rounded-lg p-4">
        <h3 className="text-xl font-semibold mb-2">Prediction</h3>
        <div className="flex items-center gap-4">
          <span className={`text-2xl font-bold ${
            patternData.prediction.includes('BULLISH') ? 'text-green-500' : 'text-red-500'
          }`}>
            {patternData.prediction}
          </span>
          <span className="text-gray-400">
            Confidence: {patternData.confidence}%
          </span>
        </div>
      </div>
    </div>
  )
}
