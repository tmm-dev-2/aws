import { useEffect, useRef } from 'react';
import { createChart, ColorType, IChartApi } from 'lightweight-charts';

interface ChartWidgetProps {
  symbol?: string;
  timeframe?: string;
  strategy?: string;
}

interface CandleData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

const ChartWidget = ({ symbol, timeframe, strategy }: ChartWidgetProps) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<any>(null);

  // Initialize chart
  useEffect(() => {
    if (chartContainerRef.current && !chartRef.current) {
      const chart = createChart(chartContainerRef.current, {
        layout: {
          background: { 
            type: 'solid', 
            color: '#131722' 
          },
          textColor: '#d1d4dc',
        },
        grid: {
          vertLines: { color: '#1e222d' },
          horzLines: { color: '#1e222d' },
        },
        width: chartContainerRef.current.clientWidth,
        height: chartContainerRef.current.clientHeight,
      });

      chartRef.current = chart;

      // Create candlestick series
      const candlestickSeries = chart.createCandlestickSeries({
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350'
      });
      
      seriesRef.current = candlestickSeries;

      // Handle window resize
      const handleResize = () => {
        if (chartRef.current && chartContainerRef.current) {
          chartRef.current.applyOptions({
            width: chartContainerRef.current.clientWidth,
            height: chartContainerRef.current.clientHeight,
          });
        }
      };

      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        if (chartRef.current) {
          chartRef.current.remove();
          chartRef.current = null;
        }
      };
    }
  }, []);

  // Fetch and update data when props change
  useEffect(() => {
    const fetchData = async () => {
      if (!symbol || !timeframe) return;

      try {
        const response = await fetch(`/api/fetch_candles?symbol=${symbol}&timeframe=${timeframe}`);
        if (!response.ok) throw new Error('Failed to fetch data');
        
        const rawData = await response.json();
        
        // Transform data to match lightweight-charts format
        const formattedData = rawData.map((candle: CandleData) => ({
          time: candle.timestamp,
          open: candle.open,
          high: candle.high,
          low: candle.low,
          close: candle.close
        }));
        
        if (seriesRef.current) {
          seriesRef.current.setData(formattedData);
        }
      } catch (error) {
        console.error('Error fetching candle data:', error);
      }
    };

    fetchData();
  }, [symbol, timeframe]);

  // Update strategy visualization when strategy changes
  useEffect(() => {
    if (strategy && strategy !== 'none') {
      const fetchStrategyData = async () => {
        try {
          const response = await fetch(
            `/api/apply_strategy?symbol=${symbol}&timeframe=${timeframe}&strategy=${strategy}`
          );
          if (!response.ok) throw new Error('Failed to fetch strategy data');
          
          const strategyData = await response.json();
          
          // Add markers or indicators based on strategy data
          if (seriesRef.current && strategyData.signals) {
            const markers = strategyData.signals.map((signal: any) => ({
              time: signal.timestamp,
              position: signal.type === 'buy' ? 'belowBar' : 'aboveBar',
              color: signal.type === 'buy' ? '#26a69a' : '#ef5350',
              shape: signal.type === 'buy' ? 'arrowUp' : 'arrowDown',
              text: signal.type.toUpperCase()
            }));
            
            seriesRef.current.setMarkers(markers);
          }
        } catch (error) {
          console.error('Error fetching strategy data:', error);
        }
      };

      fetchStrategyData();
    } else {
      // Clear strategy visualization
      if (seriesRef.current) {
        seriesRef.current.setMarkers([]);
      }
    }
  }, [strategy, symbol, timeframe]);

  return (
    <div 
      ref={chartContainerRef} 
      className="w-full h-[calc(100vh-48px)] bg-[#131722]"
    />
  );
};

export default ChartWidget; 