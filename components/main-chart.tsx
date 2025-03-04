"use client"

import { useEffect, useRef, useState } from 'react'
import { createChart, ColorType, IChartApi, LineStyle, ISeriesApi, SeriesOptions, MouseEventParams } from 'lightweight-charts';
import { DoubleHullTurboP1Chart } from '../strategies/double-hull-turbo-p1/double-hull-turbo-p1';
import { KernelRegressionChart } from '../strategies/kernel-regression-p1/kernel-regression-p1';
import { DrawingTools } from './drawing-tools';
import { SymbolSearch } from '../components/SymbolSearch';
import { Settings } from 'lucide-react';

interface CandleData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface ActiveIndicator {
  id: string;
  name: string;
  series: ISeriesApi<'Line'>;
  settings: Record<string, any>;
  script: string;
}

interface MainChartProps {
  symbol: string;
  selectedPeriod: string;
  selectedStrategy: string;
  data?: CandleData[];
  onAnalysisResults?: (results: any) => void;
}

interface MainChartContainerProps {
  layout: string;
  symbols: string[];
  selectedPeriod: string;
  selectedStrategy: string;
  onAnalysisResults?: (results: any) => void;
}

interface ChartInstanceProps {
  symbol: string;
  selectedPeriod: string;
  selectedStrategy: string;
  index: number;
  onAnalysisResults?: (results: any) => void;
}

const ChartInstance: React.FC<ChartInstanceProps> = ({ 
  symbol, 
  selectedPeriod, 
  selectedStrategy, 
  index,
  onAnalysisResults 
}) => {
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'candlestick'> | null>(null);
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [chartData, setChartData] = useState<CandleData[]>([]);
  const [activeIndicators, setActiveIndicators] = useState<ActiveIndicator[]>([]);
  const [showIndicatorSettings, setShowIndicatorSettings] = useState<string | null>(null);
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

  const handleScriptResults = (scriptData: { script: string, name: string, type: string, settings: any, data: any[] }) => {
    if (!chartRef.current || !currentData.length) return;

    const indicatorId = Date.now().toString();
    const indicatorSeries = chartRef.current.addLineSeries({
      color: 'rgba(41, 98, 255, 1)',
      lineWidth: 2,
      ...scriptData.settings?.style
    });

    const indicatorData = scriptData.data.map((value: number, index: number) => ({
      time: currentData[index].time / 1000,
      value
    }));

    indicatorSeries.setData(indicatorData);

    setActiveIndicators(prev => [...prev, {
      id: indicatorId,
      name: scriptData.name,
      series: indicatorSeries,
      settings: scriptData.settings,
      script: scriptData.script
    }]);
  };

  const updateIndicatorSettings = async (indicatorId: string, newSettings: Record<string, any>) => {
    const indicator = activeIndicators.find(ind => ind.id === indicatorId);
    if (!indicator) return;

    try {
      const response = await fetch('http://localhost:5001/run_script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          script: indicator.script,
          settings: newSettings,
          data: currentData
        })
      });

      const results = await response.json();
      const updatedData = results.map((value: number, index: number) => ({
        time: currentData[index].time / 1000,
        value
      }));

      indicator.series.setData(updatedData);
      
      setActiveIndicators(prev => prev.map(ind => 
        ind.id === indicatorId 
          ? { ...ind, settings: newSettings }
          : ind
      ));
    } catch (error) {
      console.error('Error updating indicator:', error);
    }
  };

  const removeIndicator = (indicatorId: string) => {
    const indicator = activeIndicators.find(ind => ind.id === indicatorId);
    if (indicator && chartRef.current) {
      chartRef.current.removeSeries(indicator.series);
      setActiveIndicators(prev => prev.filter(ind => ind.id !== indicatorId));
    }
  };

  const fetchCandleData = async (sym: string) => {
    try {
      const response = await fetch(
        `http://localhost:5000/fetch_candles?symbol=${sym}&timeframe=${selectedPeriod}`
      );
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      if (data && Array.isArray(data)) {
        setCurrentData(data);
        updateChart(data);
      }
    } catch (error) {
      console.error('Error fetching candle data:', error);
    }
  };

  const handleSymbolSelect = async (newSymbol: string) => {
    setCurrentSymbol(newSymbol);
    fetchCandleData(newSymbol);
    setShowSearch(false);
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

    // Update all active indicators with new data
    activeIndicators.forEach(indicator => {
      updateIndicatorSettings(indicator.id, indicator.settings);
    });
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
      },
      grid: {
        vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
        horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: '#2a2e39',
        textColor: '#d1d4dc',
      },
    });

    const candleSeries = chart.addCandlestickSeries();
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

    return () => {
      resizeObserver.disconnect();
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

  return (
    <div className="flex flex-col h-full border border-[#2a2e39]">
      <div className="px-3 py-2 border-b border-[#2a2e39] flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div 
            className="cursor-pointer hover:bg-[#2a2e39] p-1 rounded"
            onClick={() => setShowSearch(true)}
          >
            <span className="font-bold">{currentSymbol}</span>
          </div>
          <div className="flex gap-2">
            {activeIndicators.map(indicator => (
              <div key={indicator.id} className="flex items-center bg-[#2a2e39] rounded px-2 py-1">
                <span className="text-white text-sm">{indicator.name}</span>
                <button
                  onClick={() => setShowIndicatorSettings(
                    showIndicatorSettings === indicator.id ? null : indicator.id
                  )}
                  className="ml-2 text-gray-400 hover:text-white"
                >
                  <Settings size={14} />
                </button>
                <button
                  onClick={() => removeIndicator(indicator.id)}
                  className="ml-2 text-gray-400 hover:text-red-500"
                >
                  ×
                </button>
                {showIndicatorSettings === indicator.id && (
                  <div className="absolute mt-24 bg-[#2D2D2D] rounded shadow-lg p-2 z-50">
                    {Object.entries(indicator.settings?.inputs || {}).map(([key, value]) => (
                      <div key={key} className="flex items-center gap-2 mb-2">
                        <label className="text-white text-sm">{key}</label>
                        <input
                          type="number"
                          value={value}
                          onChange={(e) => updateIndicatorSettings(indicator.id, {
                            ...indicator.settings,
                            inputs: {
                              ...indicator.settings.inputs,
                              [key]: parseFloat(e.target.value)
                            }
                          })}
                          className="bg-[#1E1E1E] text-white rounded px-1 w-20"
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
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
      <div ref={chartContainerRef} className="flex-1" />
      <SymbolSearch 
        isOpen={showSearch}
        onClose={() => setShowSearch(false)}
        onSymbolSelect={handleSymbolSelect}
      />
    </div>
  );
};

export const MainChartContainer: React.FC<MainChartContainerProps> = ({
  layout,
  symbols,
  selectedPeriod,
  selectedStrategy,
  onAnalysisResults
}) => {
  return (
    <div className="h-full">
      <div className="grid grid-cols-1 grid-rows-1 h-full">
        {symbols.map((symbol, index) => (
          <ChartInstance
            key={`${symbol}-${index}`}
            symbol={symbol}
            selectedPeriod={selectedPeriod}
            selectedStrategy={selectedStrategy}
            index={index}
            onAnalysisResults={onAnalysisResults}
          />
        ))}
      </div>
      </div>
  );
};

export default MainChartContainer;
