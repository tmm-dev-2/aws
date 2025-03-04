"use client"

import { useState, useEffect } from 'react'
import { NavigationBar } from './navigation-bar'
import { MainView } from './main-view'

interface AnalysisData {
  patterns: {
    [key: string]: {
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
  }
  indicators: {
    [key: string]: any
  }
  drawings: {
    [key: string]: any
  }
}

export const AIResults = () => {
  const [selectedPattern, setSelectedPattern] = useState<string>('')
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchAnalysisData()
  }, [])

  const fetchAnalysisData = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:5000/analyze')
      const data = await response.json()
      setAnalysisData(data)
    } catch (error) {
      console.error('Error fetching analysis data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePatternSelect = (patternId: string) => {
    setSelectedPattern(patternId)
  }

  if (loading) {
    return <div className="flex items-center justify-center h-full">Loading...</div>
  }

  return (
    <div className="flex h-full bg-[#1A1A1A] text-white">
      <NavigationBar 
        onPatternSelect={handlePatternSelect}
        patterns={analysisData?.patterns || {}}
      />
      <MainView 
        patternId={selectedPattern}
        patternData={analysisData?.patterns[selectedPattern]}
      />
    </div>
  )
}
