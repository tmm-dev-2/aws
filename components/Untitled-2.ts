"use client"

import { useEffect, useRef, useState, useLayoutEffect } from 'react'
import { createChart, ColorType, IChartApi, LineStyle, ISeriesApi, SeriesOptions, MouseEventParams } from 'lightweight-charts';
import { DoubleHullTurboP1Chart } from '../strategies/double-hull-turbo-p1/double-hull-turbo-p1';
import { KernelRegressionChart } from '../strategies/kernel-regression-p1/kernel-regression-p1';
import { DrawingTools } from './drawing-tools';
import { SymbolSearch } from '../components/SymbolSearch';
import { ChevronDown } from 'lucide-react';

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

interface MainChartContainerProps {
  layout: string;
  symbols: string[];
  selectedPeriod: string;
  selectedStrategy: string;
}

interface ChartInstanceProps {
  symbol: string;
  selectedPeriod: string;
  selectedStrategy: string;
  index: number;
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
  const [analysisResults, setAnalysisResults] = useState(null);

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
      priceScaleId: 'right',
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

    chartContainerRef.current.addEventListener('resize', handleResize);

    return () => {
      resizeObserver.disconnect();
      chartContainerRef.current?.removeEventListener('resize', handleResize);
    };
  }, []);

  useEffect(() => {
    if (!chartRef.current) return;

    const handleAnalysis = async () => {
      try {
        const response = await fetch(`http://localhost:5000/analyze?symbol=${currentSymbol}`);
        if (!response.ok) throw new Error('Analysis failed');
        const data = await response.json();
        setAnalysisResults(data);
      } catch (error) {
        console.error('Analysis error:', error);
      }
    };

    const codeLlamaIcon = document.createElement('div');
    codeLlamaIcon.innerHTML = '🤖';
    codeLlamaIcon.style.position = 'absolute';
    codeLlamaIcon.style.top = '10px';
    codeLlamaIcon.style.left = '10px';
    codeLlamaIcon.style.fontSize = '20px';
    codeLlamaIcon.style.cursor = 'pointer';
    codeLlamaIcon.style.zIndex = '1000';
    codeLlamaIcon.title = 'Technical Analysis';
    codeLlamaIcon.onclick = handleAnalysis;

    chartContainerRef.current?.appendChild(codeLlamaIcon);

    return () => {
      codeLlamaIcon?.remove();
    };
  }, [currentSymbol]);

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
      
      {analysisResults && (
        <div className="absolute top-12 right-4 bg-[#2D2D2D] p-4 rounded shadow-lg max-w-md">
          <h3 className="text-sm font-bold mb-2">Analysis Results</h3>
          <pre className="text-xs overflow-auto max-h-60">
            {JSON.stringify(analysisResults, null, 2)}
          </pre>
        </div>
      )}
      
      <SymbolSearch 
        isOpen={showSearch}
        onClose={() => setShowSearch(false)}
        onSymbolSelect={(newSymbol) => {
          setCurrentSymbol(newSymbol);
          fetchCandleData(newSymbol);
          setShowSearch(false);
        }}
      />
    </div>
  );
};

export const MainChartContainer: React.FC<MainChartContainerProps> = ({
  layout,
  symbols,
  selectedPeriod,
  selectedStrategy,
}) => {
  const [showLayoutMenu, setShowLayoutMenu] = useState(false);
  const gridClass = getGridClass(layout);

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-2 border-b border-[#2a2e39]">
        <div className="relative">
          <button
            className="flex items-center gap-2 px-3 py-1.5 text-sm bg-[#2a2e39] rounded hover:bg-[#363c4e]"
            onClick={() => setShowLayoutMenu(!showLayoutMenu)}
          >
            Layout <ChevronDown className="w-4 h-4" />
          </button>
          {showLayoutMenu && (
            <div className="absolute top-full left-0 mt-1 bg-[#1A1A1A] border border-[#2a2e39] rounded shadow-lg z-50">
              {layoutOptions.map((option) => (
                <button
                  key={option.id}
                  className="block w-full px-4 py-2 text-left text-sm hover:bg-[#2a2e39]"
                  onClick={() => {
                    // Handle layout change
                    setShowLayoutMenu(false);
                  }}
                >
                  {option.name}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
      <div className={`grid flex-1 gap-[1px] bg-[#2a2e39] ${gridClass}`}>
        {symbols.map((symbol, index) => (
          <ChartInstance
            key={`${symbol}-${index}`}
            symbol={symbol}
            selectedPeriod={selectedPeriod}
            selectedStrategy={selectedStrategy}
            index={index}
          />
        ))}
      </div>
    </div>
  );
};