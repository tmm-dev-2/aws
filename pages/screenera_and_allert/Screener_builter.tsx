import React, { useState } from 'react';

interface Props {
  onScreenerSubmit: (formula: string, country: string, segment: string, timeframe: string) => void;
}

export const ScreenerBuilder: React.FC<Props> = ({ onScreenerSubmit }) => {
  const [screenerFormula, setScreenerFormula] = useState<string>('');
  const [selectedCountry, setSelectedCountry] = useState<string>('IN');
  const [selectedSegment, setSelectedSegment] = useState<string>('FUT');
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('1D');

  const technicalIndicators = {
    Price: ['open', 'high', 'low', 'close', 'volume'],
    Trend: ['Sma', 'Ema', 'Wma', 'Hma', 'SuperTrend', 'Alma', 'LinReg', 'Vwma'],
    Momentum: ['Rsi', 'Macd', 'Stoch', 'Mfi', 'Cci', 'Wpr', 'Mom', 'Roc', 'Tsi'],
    Volatility: ['Atr', 'Bb', 'Bbw', 'Kc', 'Kcw', 'Stdev', 'Variance'],
    Volume: ['AccDist', 'OBV', 'PVT', 'VWAP', 'WAD', 'WVAD', 'NVI', 'PVI'],
    Pattern: ['PivotHigh', 'PivotLow', 'Cross', 'Crossover', 'Crossunder']
  };

  const operators = [
    'and', 'or', 'not',
    'cross above', 'cross below',
    '>', '<', '>=', '<=', '=', 
    '+', '-', '*', '/',
    '(', ')', ','
  ];

  const handleIndicatorClick = (indicator: string) => {
    setScreenerFormula(prev => `${prev} ${indicator}`);
  };

  const handleOperatorClick = (operator: string) => {
    setScreenerFormula(prev => `${prev} ${operator}`);
  };

  const handleRunScan = () => {
    onScreenerSubmit(screenerFormula, selectedCountry, selectedSegment, selectedTimeframe);
  };

  const handleClear = () => {
    setScreenerFormula('');
  };

  return (
    <div className="screener-container">
      <div className="header-section">
        <h2>Technical Screener</h2>
        <div className="market-selectors">
          <select value={selectedCountry} onChange={(e) => setSelectedCountry(e.target.value)}>
            <option value="IN">India</option>
            <option value="US">United States</option>
          </select>
          
          <select value={selectedSegment} onChange={(e) => setSelectedSegment(e.target.value)}>
            <option value="EQ">Equity</option>
            <option value="FUT">Futures</option>
            <option value="OPT">Options</option>
            <option value="IDX">Indices</option>
            <option value="CURR">Currency</option>
            <option value="COMM">Commodities</option>
          </select>

          <select value={selectedTimeframe} onChange={(e) => setSelectedTimeframe(e.target.value)}>
            <option value="1m">1 Minute</option>
            <option value="5m">5 Minutes</option>
            <option value="15m">15 Minutes</option>
            <option value="1h">1 Hour</option>
            <option value="4h">4 Hours</option>
            <option value="1D">Daily</option>
            <option value="1W">Weekly</option>
          </select>
        </div>
      </div>

      <div className="screener-layout">
        <div className="left-panel">
          {Object.entries(technicalIndicators).map(([category, indicators]) => (
            <div key={category} className="indicator-category">
              <h3>{category}</h3>
              <div className="indicator-list">
                {indicators.map(indicator => (
                  <button 
                    key={indicator}
                    onClick={() => handleIndicatorClick(indicator)}
                    className="indicator-btn"
                  >
                    {indicator}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="right-panel">
          <div className="formula-editor">
            <textarea
              value={screenerFormula}
              onChange={(e) => setScreenerFormula(e.target.value)}
              placeholder="Build your screening formula..."
              rows={10}
              className="formula-input"
            />
          </div>

          <div className="operators-panel">
            {operators.map(operator => (
              <button 
                key={operator}
                onClick={() => handleOperatorClick(operator)}
                className="operator-btn"
              >
                {operator}
              </button>
            ))}
          </div>

          <div className="action-buttons">
            <button onClick={handleRunScan} className="submit-btn">Run Scan</button>
            <button onClick={handleClear} className="clear-btn">Clear</button>
          </div>
        </div>
      </div>

      <style jsx>{`
        .screener-container {
          background: #1e222d;
          color: #e0e3eb;
          padding: 20px;
          border-radius: 8px;
        }
        .header-section {
          margin-bottom: 20px;
        }
        .market-selectors {
          display: flex;
          gap: 10px;
          margin-bottom: 20px;
        }
        .market-selectors select {
          background: #2a2e39;
          color: #e0e3eb;
          border: 1px solid #363c4e;
          padding: 8px;
          border-radius: 4px;
        }
        .screener-layout {
          display: grid;
          grid-template-columns: 300px 1fr;
          gap: 20px;
        }
        .left-panel {
          background: #2a2e39;
          padding: 15px;
          border-radius: 6px;
          height: calc(100vh - 200px);
          overflow-y: auto;
        }
        .indicator-category {
          margin-bottom: 20px;
        }
        .indicator-category h3 {
          color: #788195;
          margin-bottom: 10px;
        }
        .indicator-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
          gap: 8px;
        }
        .indicator-btn {
          background: #363c4e;
          color: #e0e3eb;
          border: none;
          padding: 8px;
          border-radius: 4px;
          cursor: pointer;
          text-align: left;
          transition: background 0.2s;
        }
        .indicator-btn:hover {
          background: #404859;
        }
        .right-panel {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }
        .formula-editor {
          flex-grow: 1;
        }
        .formula-input {
          width: 100%;
          height: 100%;
          min-height: 200px;
          background: #2a2e39;
          color: #e0e3eb;
          border: 1px solid #363c4e;
          border-radius: 4px;
          padding: 12px;
          font-family: monospace;
          resize: vertical;
        }
        .operators-panel {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          padding: 10px;
          background: #2a2e39;
          border-radius: 4px;
        }
        .operator-btn {
          background: #363c4e;
          color: #e0e3eb;
          border: none;
          padding: 8px 12px;
          border-radius: 4px;
          cursor: pointer;
          transition: background 0.2s;
        }
        .operator-btn:hover {
          background: #404859;
        }
        .action-buttons {
          display: flex;
          gap: 10px;
          justify-content: flex-end;
        }
        .submit-btn, .clear-btn {
          padding: 10px 20px;
          border-radius: 4px;
          border: none;
          cursor: pointer;
          font-weight: 500;
          color: white;
        }
        .submit-btn {
          background: #2962ff;
        }
        .clear-btn {
          background: #f44336;
        }
        .submit-btn:hover {
          background: #1e4bd8;
        }
        .clear-btn:hover {
          background: #d32f2f;
        }
      `}</style>
    </div>
  );
};
