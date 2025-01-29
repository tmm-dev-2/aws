"use client"

import { useEffect, useRef, useState } from 'react'
import { createChart, ColorType, IChartApi, LineStyle, ISeriesApi, SeriesOptions, Time } from 'lightweight-charts';
import { DoubleHullTurboP1Chart } from '../strategies/double-hull-turbo-p1/double-hull-turbo-p1';
import { KernelRegressionChart } from '../strategies/kernel-regression-p1/kernel-regression-p1';
import { DrawingTools } from './drawing-tools';

// Import drawing logic
import { TrendLine, Ray, ExtendedLine, TrendAngle, HorizontalLine, VerticalLine, CrossLine, LineSegment } from '../drawing-logic-tsx/lines'
import { Pitchfork, SchiffPitchfork } from '../drawing-logic-tsx/pitchfork'
import { ParallelChannel, FlatTopBottomChannel, DisjointedChannel } from '../drawing-logic-tsx/channels'
import { drawCyclicLines, drawTimeCycles, drawSineLine } from '../drawing-logic-tsx/cycles'
import { GannBox, GannSquareFixed, GannFan } from '../drawing-logic-tsx/gann'
import { drawElliotImpulseWave, drawElliotCorrectionWave, drawElliotTriangleWave, WaveResult } from '../drawing-logic-tsx/elliot-wave'
import { ArrowMarker, Arrow, ArrowMarkUp, ArrowMarkDown } from '../drawing-logic-tsx/arrows'
import { Brush, Highlighter } from '../drawing-logic-tsx/brushes'
import { rectangle, rotatedRectangle, ellipse } from '../drawing-logic-tsx/shapes'
import { calculateLongPosition, calculateShortPosition, calculateForecast } from '../drawing-logic-tsx/projection'
import { calculatePriceRange, calculateDataRange, calculateDataPriceRange } from '../drawing-logic-tsx/measurer'

interface CandleData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface MainChartProps {
  symbol: string;
  selectedPeriod: string;
  selectedStrategy: string;
  data?: CandleData[];
}

export const MainChart: React.FC<MainChartProps> = ({ 
  symbol, 
  selectedPeriod,
  selectedStrategy,
  data
}) => {
  const [chartData, setChartData] = useState<CandleData[]>([]);
  const chartContainerRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const seriesRef = useRef<ReturnType<IChartApi['addCandlestickSeries']>>(null)
  const strategyChartRef = useRef<DoubleHullTurboP1Chart | KernelRegressionChart | null>(null)
  const [activeDrawingTool, setActiveDrawingTool] = useState<string | null>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [drawingPoints, setDrawingPoints] = useState([{x: 0, y: 0}]);
  const drawingSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);

  // Initialize chart
  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 570,
      layout: {
        background: { color: '#131722' },
        textColor: '#d1d4dc',
      },
      grid: {
        vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
        horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: '#4CAF50',
      downColor: '#FF5252',
      borderVisible: false,
      wickUpColor: '#4CAF50',
      wickDownColor: '#FF5252',
    });

    chartRef.current = chart;
    seriesRef.current = candleSeries;

    return () => {
      if (strategyChartRef.current) {
        strategyChartRef.current.remove();
      }
      chart.remove();
    };
  }, []);

  // Handle strategy changes
  useEffect(() => {
    if (!chartRef.current || !symbol || !selectedPeriod) return;

    // Cleanup previous strategy chart if exists
    if (strategyChartRef.current) {
      strategyChartRef.current.remove();
      strategyChartRef.current = null;
    }

    if (selectedStrategy === 'double-hull-turbo-p1') {
      strategyChartRef.current = new DoubleHullTurboP1Chart(chartRef.current);
      strategyChartRef.current.updateChart(symbol, selectedPeriod);
    } else if (selectedStrategy === 'kernel-regression-p1') {
      strategyChartRef.current = new KernelRegressionChart(chartRef.current);
      strategyChartRef.current.updateChart(symbol, selectedPeriod);
    }
  }, [symbol, selectedPeriod, selectedStrategy]);