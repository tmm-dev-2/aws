import React, { useState } from 'react';
import { ScreenerBuilder } from './screenera_and_allert/Screener_builter';

interface MarketData {
    open: number[];
    high: number[];
    low: number[];
    close: number[];
    volume: number[];
    timestamp: number[];
}

interface SegmentData {
    country: string;
    segment: string;
    timeframe: string;
    data: Record<string, MarketData>;
}

interface ScreenerResults {
    filtered_symbols: string[];
    segment_data: SegmentData;
}

export default function Screener() {
  const [filteredResults, setFilteredResults] = useState<string[]>([]);
  const [segmentData, setSegmentData] = useState<SegmentData | null>(null);

  const handleScreenerSubmit = async (
    formula: string, 
    country: string, 
    segment: string,
    timeframe: string
  ) => {
    try {
        const response = await fetch('/api/runScreener', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formula, country, segment, timeframe }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`API error! status: ${response.status}, message: ${errorData.error}`);
        }

        const data = await response.json();
        const results: ScreenerResults = data.results;

        setFilteredResults(results.filtered_symbols);
        setSegmentData(results.segment_data);

    } catch (error) {
      console.error("Error during screener submit:", error);
    }
  };

  return (
    <div className="screener-page">
      <ScreenerBuilder onScreenerSubmit={handleScreenerSubmit} />
    
      <div className="results-section">
        <h2>Screener Results</h2>
        <div className="results-header">
          <span>Found {filteredResults.length} matches</span>
          {segmentData && (
            <span>
              {segmentData.country} - {segmentData.segment}
            </span>
          )}
        </div>
        <div className="results-grid">
          {filteredResults.map(symbol => {
            const data = segmentData?.data[symbol];
            return (
              <div key={symbol} className="stock-result">
                <h3>{symbol}</h3>
                {data && (
                  <>
                    <div>Last Price: {data.close[data.close.length - 1]}</div>
                    <div>Volume: {data.volume[data.volume.length - 1]}</div>
                    {data.close.length > 1 && (
                        <div>Change: {((data.close[data.close.length - 1] - data.close[data.close.length - 2]) / data.close[data.close.length - 2] * 100).toFixed(2)}%</div>
                    )}
                  </>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <style jsx>{`
        .screener-page {
          padding: 20px;
          background: #1e222d;
          min-height: 100vh;
        }
        .results-section {
          margin-top: 20px;
          background: #2a2e39;
          border-radius: 8px;
          padding: 20px;
        }
        .results-header {
          display: flex;
          justify-content: space-between;
          margin-bottom: 20px;
          color: #e0e3eb;
        }
        .results-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 20px;
        }
        .stock-result {
          padding: 15px;
          background: #363c4e;
          border-radius: 8px;
          color: #e0e3eb;
        }
        .stock-result h3 {
          margin: 0 0 10px 0;
          color: #2962ff;
        }
      `}</style>
    </div>
  );
}
