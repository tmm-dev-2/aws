"use client"

import { useEffect, useRef, useState, useLayoutEffect } from 'react'
import { createChart, ColorType, IChartApi, LineStyle, ISeriesApi, SeriesOptions, MouseEventParams } from 'lightweight-charts';
import { DoubleHullTurboP1Chart } from '../strategies/double-hull-turbo-p1/double-hull-turbo-p1';
import { KernelRegressionChart } from '../strategies/kernel-regression-p1/kernel-regression-p1';
import { DrawingTools } from './drawing-tools';
import { SymbolSearch } from '../components/SymbolSearch';
import { ChevronDown } from 'lucide-react';

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
      height: chartContainerRef.current.clientHeight,
      layout: {
        background: { color: '#1A1A1A' },
        textColor: '#d1d4dc',
      },
      grid: {
        vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
        horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        tickMarkFormatter: (time, tickMarkType, locale) => {
          const date = new Date(time * 1000);
          return date.toLocaleDateString(locale, { month: 'short', day: 'numeric' });
        },
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
    }
  }, [symbol, selectedPeriod, selectedStrategy]);

  // Update chart data when it changes
  useEffect(() => {
    if (seriesRef.current && data && data.length > 0) {
      const formattedData = data.map(candle => ({
        time: candle.time / 1000, // Convert milliseconds to seconds
        open: candle.open,
        high: candle.high,
        low: candle.low,
        close: candle.close
      }));

      setChartData(data);
      seriesRef.current.setData(formattedData);

      const lastTimestamp = data[data.length - 1].time / 1000; // Convert milliseconds to seconds
      const sixMonthsAgo = lastTimestamp - (180 * 24 * 60 * 60);
      chartRef.current?.timeScale().setVisibleRange({
        from: sixMonthsAgo,
        to: lastTimestamp
      });
    }
  }, [data]);

  // Handle window resize using ResizeObserver
  useLayoutEffect(() => {
    if (!chartContainerRef.current || !chartRef.current) return;

    const handleResize = () => {
      const parent = chartContainerRef.current?.parentElement;
      if (parent && chartRef.current) {
        chartRef.current.resize(
          parent.clientWidth,
          parent.clientHeight
        );
        
        // Update strategy chart if exists
        if (strategyChartRef.current) {
          strategyChartRef.current.resize(
            parent.clientWidth,
            parent.clientHeight
          );
        }
      }
    };

    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(chartContainerRef.current);

    return () => {
      resizeObserver.disconnect();
    };
  }, []);

  // Fetch and update data if no data prop is provided
  useEffect(() => {
    const fetchData = async () => {
      if (!symbol || !selectedPeriod || data) return;
  
      try {
        const response = await fetch(
          `http://localhost:5000/fetch_candles?symbol=${symbol}&timeframe=${selectedPeriod}`
        );
        if (!response.ok) throw new Error('Failed to fetch data');
        
        const rawData = await response.json();
        
        // Aggregate data based on selected timeframe
        const aggregatedData = aggregateCandles(rawData, selectedPeriod);
        
        // Convert CandleData to the format expected by lightweight-charts
        const formattedData = aggregatedData.map(candle => ({
          time: candle.time,
          open: candle.open,
          high: candle.high,
          low: candle.low,
          close: candle.close
        }));
        
        setChartData(aggregatedData);
        seriesRef.current?.setData(formattedData);
      } catch (error) {
        console.error('Error fetching candle data:', error);
      }
    };
  
    // Function to aggregate candles based on timeframe
    const aggregateCandles = (data: CandleData[], timeframe: string): CandleData[] => {
      const aggregationMap: { [key: string]: number } = {
        '1d': 86400,    // 1 day
        '2d': 172800,   // 2 days
        '1w': 604800,   // 1 week
        '2w': 1209600,  // 2 weeks
        '1m': 2592000,  // 1 month (approx)
        '2m': 5184000,  // 2 months (approx)
        '3m': 7776000,  // 3 months (approx)
        '6m': 15552000, // 6 months (approx)
        '1y': 31536000, // 1 year (approx)
        '2y': 63072000  // 2 years (approx)
      };
  
      const periodSeconds = aggregationMap[timeframe];
      if (!periodSeconds) return data;
  
      const aggregatedCandles: CandleData[] = [];
      let currentPeriodStart = data[0].time;
      let currentOpen = data[0].open;
      let currentHigh = data[0].high;
      let currentLow = data[0].low;
      let currentClose = data[0].close;
      let currentVolume = data[0].volume;
  
      for (let i = 1; i < data.length; i++) {
        const candle = data[i];
        
        if (candle.time - currentPeriodStart >= periodSeconds) {
          // Close the current period's candle
          aggregatedCandles.push({
            time: currentPeriodStart,
            open: currentOpen,
            high: currentHigh,
            low: currentLow,
            close: currentClose,
            volume: currentVolume
          });
  
          // Start a new period
          currentPeriodStart = candle.time;
          currentOpen = candle.open;
          currentHigh = candle.high;
          currentLow = candle.low;
          currentClose = candle.close;
          currentVolume = candle.volume;
        } else {
          // Update current period's data
          currentHigh = Math.max(currentHigh, candle.high);
          currentLow = Math.min(currentLow, candle.low);
          currentClose = candle.close;
          currentVolume += candle.volume;
        }
      }
  
      // Add the last period's candle
      aggregatedCandles.push({
        time: currentPeriodStart,
        open: currentOpen,
        high: currentHigh,
        low: currentLow,
        close: currentClose,
        volume: currentVolume
      });
  
      return aggregatedCandles;
    };
  
    fetchData();
  
    // Add event listener for period change
    const handlePeriodChange = (event: CustomEvent) => {
      const { symbol: eventSymbol, period } = event.detail;
      if (eventSymbol === symbol) {
        fetchData();
      }
    };
  
    window.addEventListener('periodChange', handlePeriodChange as EventListener);
  
    // Cleanup event listener
    return () => {
      window.removeEventListener('periodChange', handlePeriodChange as EventListener);
    };
  }, [symbol, selectedPeriod, selectedStrategy, data]);

  return (
    <div 
      ref={chartContainerRef} 
      className="w-full h-full overflow-hidden"
     style={{ position: 'relative' }}
    />
  )
  // Handle drawing tool interactions
useEffect(() => {
  if (!chartContainerRef.current || !chartRef.current) return;

  const handleMouseDown = (e: MouseEvent) => {
    if (!activeDrawingTool) return;
    
    const rect = chartContainerRef.current!.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    setIsDrawing(true);
    setDrawingPoints([{x, y}]);
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDrawing || !activeDrawingTool || !drawingSeriesRef.current) return;

    const rect = chartContainerRef.current!.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const points = [...drawingPoints, {x, y}];
    setDrawingPoints(points);

    // Convert screen coordinates to chart coordinates
      const chartPoints = points.map(point => {
      const timePoint = Math.floor(point.x);
      const pricePoint = point.y;
      return {
        time: timePoint as number,
        value: pricePoint as number
      };
      });

      switch (activeDrawingTool) {
          case 'trendLine':
            if (points.length >= 2) {
              const trendLine = new TrendLine(points[0], points[points.length - 1]);
              const linePoints = trendLine.getExtendedPoints();
              const chartLinePoints = linePoints.map(point => ({
                time: Math.floor(point.x),
                value: point.y
              }));
              drawingSeriesRef.current.setData(chartLinePoints);
            }
            break;
          case 'ray':
            if (points.length >= 2) {
              const ray = new Ray(points[0], points[points.length - 1]);
              const extendedPoints = ray.getExtendedPoints();
              const chartLinePoints = extendedPoints.map(point => ({
                time: Math.floor(point.x),
                value: point.y
              }));
              drawingSeriesRef.current.setData(chartLinePoints);
            }
            break;
          case 'extendedLine':
               if (points.length >= 2) {
                  const linePoints = new ExtendedLine(points[0], points[points.length - 1]);
                   const chartLinePoints = linePoints.getExtendedPoints().map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'trendAngle':
               if (points.length >= 2) {
                  const linePoints = new TrendAngle(points[0], points[points.length - 1]);
                   const chartLinePoints = [{
                      time: Math.floor(points[0].x),
                      value: points[0].y
                  },
                  {
                      time: Math.floor(points[points.length - 1].x),
                      value: points[points.length - 1].y
                  }];
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'horizontalLine':
               if (points.length >= 1) {
                  const linePoints = new HorizontalLine(points[0].y);
                   const chartLinePoints = linePoints.getExtendedPoints().map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'verticalLine':
               if (points.length >= 1) {
                  const linePoints = new VerticalLine(points[0].x);
                   const chartLinePoints = linePoints.getExtendedPoints().map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'crossLine':
               if (points.length >= 2) {
                  const linePoints = new CrossLine(points[0].x, points[0].y);
                   const chartLinePoints = [linePoints.getPoints()].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'pitchfork':
              if (points.length >= 3) {
                  const linePoints = new Pitchfork(points[0].x, points[0].y, points[1].x, points[1].y, points[2].x, points[2].y);
                   const chartLinePoints = linePoints.getLines().map(line => ({
                      time: Math.floor(line.startPoint.x),
                      value: line.startPoint.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'schiffPitchfork':
               if (points.length >= 3) {
                  const linePoints = new SchiffPitchfork(points[0].x, points[0].y, points[1].x, points[1].y, points[2].x, points[2].y);
                   const chartLinePoints = linePoints.getLines().map(line => ({
                      time: Math.floor(line.startPoint.x),
                      value: line.startPoint.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'parallelChannel':
               if (points.length >= 2) {
                  const linePoints = new ParallelChannel(points[0].x, points[0].y, points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].y, points[points.length - 1].x, points[points.length - 1].y);
                   const chartLinePoints = [linePoints.draw()].map(point => ({
                      time: Math.floor(points[0].x),
                      value: points[0].y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'flatTopBottomChannel':
               if (points.length >= 2) {
                  const linePoints = new FlatTopBottomChannel(points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].x, points[points.length - 1].y, points[points.length - 1].x);
                   const chartLinePoints = [linePoints.draw()].map(point => ({
                      time: Math.floor(points[0].x),
                      value: points[0].y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'disjointedChannel':
               if (points.length >= 2) {
                  const linePoints = new DisjointedChannel(points[0].x, points[0].y, points[0].x, points[0].y, points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].y, points[points.length - 1].x, points[points.length - 1].y, points[points.length - 1].x, points[points.length - 1].y);
                   const chartLinePoints = [linePoints.draw()].map(point => ({
                      time: Math.floor(points[0].x),
                      value: points[0].y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'cyclicLines':
               if (points.length >= 2) {
                  const linePoints = drawCyclicLines(points[0].x, points[points.length - 1].x, points[0].y, points[points.length - 1].y);
                   const chartLinePoints = linePoints.map(point => ({
                      time: Math.floor(point.x1),
                      value: point.y1
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'timeCycles':
               if (points.length >= 2) {
                  const linePoints = drawTimeCycles(points[0].x, points[points.length - 1].x, points[0].y, points[points.length - 1].y);
                   const chartLinePoints = linePoints.map(point => ({
                      time: Math.floor(point.x1),
                      value: point.y1
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'sineLine':
               if (points.length >= 2) {
                  const linePoints = drawSineLine(points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].y);
                   const chartLinePoints = linePoints.map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'gannBox':
               if (points.length >= 2) {
                  const linePoints = new GannBox(points[0], points[points.length - 1]);
                   const chartLinePoints = linePoints.getLines().map(line => ({
                      time: Math.floor(line.start.x),
                      value: line.start.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'gannSquareFixed':
               if (points.length >= 2) {
                  const linePoints = new GannSquareFixed(points[0], points[points.length - 1]);
                   const chartLinePoints = linePoints.getLines().map(line => ({
                      time: Math.floor(line.start.x),
                      value: line.start.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'gannFan':
               if (points.length >= 2) {
                  const linePoints = new GannFan(points[0], points[points.length - 1]);
                   const chartLinePoints = linePoints.getLines().map(line => ({
                      time: Math.floor(line.start.x),
                      value: line.start.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'elliotImpulseWave':
               if (points.length >= 2) {
                  const linePoints = drawElliotImpulseWave(points[0], points[points.length - 1]);
                   if (linePoints && Array.isArray(linePoints.points)) {
                      const chartLinePoints = linePoints.points.map(point => ({
                          time: Math.floor(point.x),
                          value: point.y
                      }));
                      drawingSeriesRef.current.setData(chartLinePoints);
                   }
              }
              break;
          case 'elliotCorrectionWave':
               if (points.length >= 2) {
                  const linePoints = drawElliotCorrectionWave(points[0], points[points.length - 1]);
                   if (linePoints && Array.isArray(linePoints.points)) {
                      const chartLinePoints = linePoints.points.map(point => ({
                          time: Math.floor(point.x),
                          value: point.y
                      }));
                      drawingSeriesRef.current.setData(chartLinePoints);
                   }
              }
              break;
          case 'elliotTriangleWave':
               if (points.length >= 2) {
                  const linePoints = drawElliotTriangleWave(points[0], points[points.length - 1]);
                   if (linePoints && Array.isArray(linePoints.points)) {
                      const chartLinePoints = linePoints.points.map(point => ({
                          time: Math.floor(point.x),
                          value: point.y
                      }));
                      drawingSeriesRef.current.setData(chartLinePoints);
                   }
              }
              break;
          case 'arrowMarker':
               if (points.length >= 2) {
                  const linePoints = new ArrowMarker({ startX: points[0].x, startY: points[0].y, endX: points[points.length - 1].x, endY: points[points.length - 1].y });
                   const chartLinePoints = [linePoints.toObject()].map(point => ({
                      time: Math.floor(point.startX),
                      value: point.startY
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'arrow':
               if (points.length >= 2) {
                  const linePoints = new Arrow({ startX: points[0].x, startY: points[0].y, endX: points[points.length - 1].x, endY: points[points.length - 1].y });
                   const chartLinePoints = [linePoints.toObject()].map(point => ({
                      time: Math.floor(point.startX),
                      value: point.startY
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'arrowMarkUp':
               if (points.length >= 2) {
                  const linePoints = new ArrowMarkUp({ startX: points[0].x, startY: points[0].y, endX: points[points.length - 1].x, endY: points[points.length - 1].y });
                   const chartLinePoints = [linePoints.toObject()].map(point => ({
                      time: Math.floor(point.startX),
                      value: point.startY
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'arrowMarkDown':
               if (points.length >= 2) {
                  const linePoints = new ArrowMarkDown({ startX: points[0].x, startY: points[0].y, endX: points[points.length - 1].x, endY: points[points.length - 1].y });
                   const chartLinePoints = [linePoints.toObject()].map(point => ({
                      time: Math.floor(point.startX),
                      value: point.startY
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'brush':
               if (points.length >= 2) {
                  const linePoints = new Brush({ color: '#2196F3', lineThickness: 2, transparency: 1, backgroundColor: '#131722' });
                  linePoints.addPoint(points[0]);
                  linePoints.addPoint(points[points.length - 1]);
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'highlighter':
               if (points.length >= 2) {
                  const linePoints = new Highlighter({ color: '#2196F3', lineThickness: 2, transparency: 0.5, backgroundColor: '#131722' });
                  linePoints.addPoint(points[0]);
                  linePoints.addPoint(points[points.length - 1]);
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'rectangle':
               if (points.length >= 2) {
                  const linePoints = rectangle(points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].y);
                   const chartLinePoints = linePoints.shapePoints.map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'rotatedRectangle':
               if (points.length >= 2) {
                  const linePoints = rotatedRectangle(points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].y, 0);
                   const chartLinePoints = linePoints.shapePoints.map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'ellipse':
               if (points.length >= 2) {
                  const linePoints = ellipse(points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].y);
                   const chartLinePoints = linePoints.shapePoints.map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'longPosition':
               if (points.length >= 2) {
                  const linePoints = calculateLongPosition(points[0].y, points[points.length - 1].y, points[points.length - 1].y, 1);
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'shortPosition':
               if (points.length >= 2) {
                  const linePoints = calculateShortPosition(points[0].y, points[points.length - 1].y, points[points.length - 1].y, 1);
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'forecast':
               if (points.length >= 2) {
                  const linePoints = calculateForecast(points[0].y, points[points.length - 1].y, new Date(), new Date());
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'priceRange':
               if (points.length >= 2) {
                  const linePoints = calculatePriceRange(points[0].y, points[points.length - 1].y);
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'dataRange':
               if (points.length >= 2) {
                  const linePoints = calculateDataRange(new Date(), new Date());
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          case 'dataPriceRange':
               if (points.length >= 2) {
                  const linePoints = calculateDataPriceRange(new Date(), new Date(), points[0].y, points[points.length - 1].y, points[0].x, points[0].y, points[points.length - 1].x, points[points.length - 1].y);
                   const chartLinePoints = [points[0], points[points.length - 1]].map(point => ({
                      time: Math.floor(point.x),
                      value: point.y
                  }));
                  drawingSeriesRef.current.setData(chartLinePoints);
              }
              break;
          default:
              drawingSeriesRef.current.setData(chartPoints);
      }
  };

  const handleMouseUp = () => {
    if (!isDrawing || !activeDrawingTool) return;
    setIsDrawing(false);
    setDrawingPoints([]);
  };

  chartContainerRef.current.addEventListener('mousedown', handleMouseDown);
  chartContainerRef.current.addEventListener('mousemove', handleMouseMove);
  chartContainerRef.current.addEventListener('mouseup', handleMouseUp);

  return () => {
    chartContainerRef.current?.removeEventListener('mousedown', handleMouseDown);
    chartContainerRef.current?.removeEventListener('mousemove', handleMouseMove);
    chartContainerRef.current?.removeEventListener('mouseup', handleMouseUp);
  };
}, [activeDrawingTool, isDrawing, drawingPoints]);

const handleDrawingToolSelect = (tool: string, toolType?: string) => {
  setActiveDrawingTool(tool);
  if (drawingSeriesRef.current) {
    drawingSeriesRef.current.setData([]);
    
    // Initialize the appropriate drawing tool based on type
    const options = {
      lineWidth: 2,
      color: '#2196F3',
      lineStyle: LineStyle.Solid,
    };

    switch(toolType) {
      case 'lines':
        options.lineWidth = 2;
        options.color = '#2196F3';
        options.lineStyle = LineStyle.Solid;
        break;
      case 'pitchfork':
        options.lineWidth = 1;
        options.color = '#FF5252';
        options.lineStyle = LineStyle.Dashed;
        break;
      case 'fibonacci':
        options.lineWidth = 1;
        options.color = '#9C27B0';
        options.lineStyle = LineStyle.Dotted;
        break;
      case 'rectangle':
        options.lineWidth = 1;
        options.color = '#4CAF50';
        break;
      default:
        options.lineWidth = 2;
        options.color = '#2196F3';
        options.lineStyle = LineStyle.Solid;
    }
  }
};
}

interface MainChartContainerProps {
  layout: string;
  symbols: string[];
  selectedPeriod: string;
  selectedStrategy: string;
}
const layoutOptions = [
  { id: 'single', name: 'Single View', grid: 'grid-cols-1 grid-rows-1' },
  { id: 'horizontal-2', name: '2 Charts Horizontal', grid: 'grid-cols-2 grid-rows-1' },
  { id: 'vertical-2', name: '2 Charts Vertical', grid: 'grid-cols-1 grid-rows-2' },
  { id: 'triple', name: '3 Charts', grid: 'grid-cols-2 grid-rows-2' },
  { id: 'quad', name: '4 Charts', grid: 'grid-cols-2 grid-rows-2' },
  { id: 'horizontal-3', name: '3 Charts Horizontal', grid: 'grid-cols-3 grid-rows-1' },
  { id: 'vertical-3', name: '3 Charts Vertical', grid: 'grid-cols-1 grid-rows-3' }
];

const getGridClass = (layout: string) => {
  const layoutOption = layoutOptions.find(l => l.id === layout);
  return layoutOption?.grid || 'grid-cols-1 grid-rows-1';
};

interface ChartInstanceProps {
  symbol: string;
  selectedPeriod: string;
  selectedStrategy: string;
  index: number;
}

const ChartInstance: React.FC<ChartInstanceProps> = ({ symbol, selectedPeriod, selectedStrategy, index }) => {
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'candlestick'> | null>(null);
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [chartData, setChartData] = useState<CandleData[]>([]);
  const [ohlcv, setOhlcv] = useState({
    open: 0,
    high: 0,
    low: 0,
    close: 0,
    volume: 0
  });
  const [showSearch, setShowSearch] = useState(false);
  const [currentSymbol, setCurrentSymbol] = useState(symbol);
  const [currentData, setCurrentData] = useState<CandleData[]>([]);
  const [currentOHLCV, setCurrentOHLCV] = useState({
    open: 0,
    high: 0,
    low: 0,
    close: 0,
    volume: 0,
    time: 0
  });
  const [previousOHLCV, setPreviousOHLCV] = useState({
    open: 0,
    high: 0,
    low: 0,
    close: 0,
    volume: 0
  });
  const [searchResults, setSearchResults] = useState<Array<{ symbol: string, name: string }>>([]);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchCandleData = async (sym: string) => {
    try {
      const response = await fetch(
        `http://localhost:5000/fetch_candles?symbol=${sym}&timeframe=${selectedPeriod}`
      );
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      console.log(`Received data for ${sym}:`, data);
      
      if (data && Array.isArray(data)) {
        setCurrentData(data);
        updateChart(data);
      }
    } catch (error) {
      console.error('Error fetching candle data:', error);
    }
  };

  const handleSymbolSearch = async (query: string) => {
    if (query.length < 2) return;
    
    try {
      const response = await fetch(`http://localhost:5000/get_stock_suggestions?query=${query}`);
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const handleSymbolSelect = async (newSymbol: string) => {
    try {
      const response = await fetch(
        `http://localhost:5000/fetch_candles?symbol=${newSymbol}&timeframe=${selectedPeriod}`
      );
      const data = await response.json();
      setCurrentSymbol(newSymbol);
      setCurrentData(data);
      updateChart(data);
      setShowSearch(false);
    } catch (error) {
      console.error('Error fetching candle data:', error);
    }
  };

  const updateChart = (data: CandleData[]) => {
    if (!seriesRef.current) return;

    const formattedData = data.map(candle => ({
      time: candle.time / 1000,
      open: candle.open,
      high: candle.high,
      low: candle.low,
      close: candle.close
    }));

    seriesRef.current.setData(formattedData);

    // Update OHLCV with latest values
    if (data.length > 0) {
      const latest = data[data.length - 1];
      setCurrentOHLCV({
        open: latest.open,
        high: latest.high,
        low: latest.low,
        close: latest.close,
        volume: latest.volume,
        time: latest.time
      });
    }
  };

  useEffect(() => {
    fetchCandleData(currentSymbol);
  }, [currentSymbol, selectedPeriod]);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      layout: {
        background: { color: '#1A1A1A' },
        textColor: '#d1d4dc',
      },
      rightPriceScale: {
        visible: true,
        borderColor: '#2a2e39',
        scaleMargins: {
          top: 0.1,
          bottom: 0.1,
        },
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
      priceScaleId: 'right',  // Ensure each series has its own price scale
      scaleMargins: {
        top: 0.1,
        bottom: 0.1,
      },
    });

    chartRef.current = chart;
    seriesRef.current = candleSeries;

    return () => {
      chart.remove();
    };
  }, []);

  useEffect(() => {
    if (!chartRef.current || !seriesRef.current) return;

    const handleCrosshairMove = (param: MouseEventParams) => {
      if (!param.time) return;

      const timestamp = param.time * 1000;
      const candleIndex = currentData.findIndex(d => d.time === timestamp);
      
      if (candleIndex !== -1) {
        const currentCandle = currentData[candleIndex];
        const previousCandle = candleIndex > 0 ? currentData[candleIndex - 1] : currentCandle;

        setCurrentOHLCV({
          open: currentCandle.open,
          high: currentCandle.high,
          low: currentCandle.low,
          close: currentCandle.close,
          volume: currentCandle.volume,
          time: timestamp
        });

        setPreviousOHLCV({
          open: previousCandle.open,
          high: previousCandle.high,
          low: previousCandle.low,
          close: previousCandle.close,
          volume: previousCandle.volume
        });
      }
    };

    chartRef.current.subscribeCrosshairMove(handleCrosshairMove);

    return () => {
      if (chartRef.current) {
        chartRef.current.unsubscribeCrosshairMove(handleCrosshairMove);
      }
    };
  }, [currentData]);

  const getValueColor = (current: any) => {
    const isCandleGreen = current.close > current.open;
    return isCandleGreen ? 'text-green-500' : 'text-red-500';
  };

  const getVolumeColor = (current: any, previous: any) => {
    const isPriceUp = current.close > current.open;
    return isPriceUp ? 'text-green-500' : 'text-red-500';
  };

  useEffect(() => {
    if (!chartContainerRef.current || !chartRef.current) return;

    const handleResize = () => {
      const parent = chartContainerRef.current?.parentElement;
      if (parent && chartRef.current) {
        chartRef.current.resize(
          parent.clientWidth,
          parent.clientHeight
        );
      }
    };

    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(chartContainerRef.current);

    // Add event listener for manual resize triggers
    chartContainerRef.current.addEventListener('resize', handleResize);

    return () => {
      resizeObserver.disconnect();
      chartContainerRef.current?.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className="flex flex-col h-full border border-[#2a2e39]">
      <div className="px-3 py-2 border-b border-[#2a2e39] flex items-center justify-between">
        <div 
          className="flex items-center gap-2 cursor-pointer hover:bg-[#2a2e39] p-1 rounded"
          onClick={() => setShowSearch(true)}
        >
          <span className="font-bold">{currentSymbol}</span>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className={getValueColor(currentOHLCV)}>
            O: {currentOHLCV.open.toFixed(2)}
          </span>
          <span className={getValueColor(currentOHLCV)}>
            H: {currentOHLCV.high.toFixed(2)}
          </span>
          <span className={getValueColor(currentOHLCV)}>
            L: {currentOHLCV.low.toFixed(2)}
          </span>
          <span className={getValueColor(currentOHLCV)}>
            C: {currentOHLCV.close.toFixed(2)}
          </span>
          <span className={getVolumeColor(currentOHLCV, previousOHLCV)}>
            V: {currentOHLCV.volume.toLocaleString()}
          </span>
        </div>
      </div>
      <div ref={chartContainerRef} className="flex-1 chart-instance" />
      
      <SymbolSearch 
        isOpen={showSearch}
        onClose={() => setShowSearch(false)}
        onSymbolSelect={(newSymbol) => {
          setCurrentSymbol(newSymbol);
          fetchCandleData(newSymbol);
        }}
      />
    </div>
  );
};

export const MainChartContainer: React.FC<MainChartContainerProps> = ({
  layout,
  symbols,
  selectedPeriod,
  selectedStrategy
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver(() => {
      // Force resize all chart instances
      const chartElements = containerRef.current?.querySelectorAll('.chart-instance');
      chartElements?.forEach(element => {
        const event = new Event('resize');
        element.dispatchEvent(event);
      });
    });

    resizeObserver.observe(containerRef.current);

    return () => resizeObserver.disconnect();
  }, []);

  return (
    <div ref={containerRef} className={`w-full h-full grid gap-4 p-2 ${getGridClass(layout)}`}>
      {symbols.map((symbol, index) => (
        <div key={`${symbol}-${index}`} className="w-full h-full mr-8">
          <ChartInstance
            symbol={symbol}
            selectedPeriod={selectedPeriod}
            selectedStrategy={selectedStrategy}
            index={index}
          />
        </div>
      ))}
    </div>
  );
};