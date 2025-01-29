import React, { useEffect, useState } from 'react';

interface TechnicalData {
  moving_averages: {
    SMA: {
      [key: string]: number[];
    };
    EMA: {
      [key: string]: number[];
    };
    ICHIMOKU: {
      baseLine: number[];
    };
    VWMA: {
      [key: string]: number[];
    };
    HMA: {
      [key: string]: number[];
    };
  };
  oscillators: {
    RSI: number[];
    MACD: {
      macd: number[];
      signal: number[];
      hist: number[];
    };
    Stochastic: {
      slowk: number[];
      slowd: number[];
    };
    CCI: number[];
    ADX: number[];
    'Williams%R': number[];
    AO: number[];
    Momentum: number[];
    StochRSI: {
      fastk: number[];
      fastd: number[];
    };
    BullBearPower: number[];
    UltimateOscillator: number[];
  };
  pivots: {
    Classic: number[];
    Fibonacci: number[];
    Camarilla: number[];
    Woodie: number[];
    DM: number[];
  };
}

interface TechnicalsProps {
  symbol: string;
  timeframe: string;
  onClose: () => void;
}

const Technicals: React.FC<TechnicalsProps> = ({ symbol, timeframe, onClose }) => {
  const [technicalData, setTechnicalData] = useState<TechnicalData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTechnicals = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/fetch_technicals?symbol=${symbol}&timeframe=${timeframe}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setTechnicalData(data);
      } catch (err) {
        setError('Failed to fetch technical data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTechnicals();
  }, [symbol, timeframe]);

  if (loading) return <div>Loading technical analysis...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!technicalData) return <div>No technical data available</div>;

  return (
    <div className="technicals-container">
      <button onClick={onClose} className="close-button">X</button>
      
      <div className="moving-averages-section">
        <h3>Moving Averages</h3>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {technicalData.moving_averages?.SMA && Object.entries(technicalData.moving_averages.SMA).map(([period, values]) => (
              <tr key={`sma-${period}`}>
                <td>{`Simple Moving Average (${period.slice(3)})`}</td>
                <td>{values[values.length - 1]?.toFixed(2)}</td>
              </tr>
            ))}
            {technicalData.moving_averages?.EMA && Object.entries(technicalData.moving_averages.EMA).map(([period, values]) => (
              <tr key={`ema-${period}`}>
                <td>{`Exponential Moving Average (${period.slice(3)})`}</td>
                <td>{values[values.length - 1]?.toFixed(2)}</td>
              </tr>
            ))}
            {technicalData.moving_averages?.ICHIMOKU && (
              <tr>
                <td>Ichimoku Base Line (9, 26, 52, 26)</td>
                <td>{technicalData.moving_averages.ICHIMOKU.baseLine[technicalData.moving_averages.ICHIMOKU.baseLine.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.moving_averages?.VWMA && Object.entries(technicalData.moving_averages.VWMA).map(([period, values]) => (
              <tr key={`vwma-${period}`}>
                <td>{`Volume Weighted Moving Average (${period.slice(4)})`}</td>
                <td>{values[values.length - 1]?.toFixed(2)}</td>
              </tr>
            ))}
            {technicalData.moving_averages?.HMA && Object.entries(technicalData.moving_averages.HMA).map(([period, values]) => (
              <tr key={`hma-${period}`}>
                <td>{`Hull Moving Average (${period.slice(3)})`}</td>
                <td>{values[values.length - 1]?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="oscillators-section">
        <h3>Oscillators</h3>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {technicalData.oscillators?.RSI && (
              <tr>
                <td>RSI (14)</td>
                <td>{technicalData.oscillators.RSI[technicalData.oscillators.RSI.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.MACD && (
              <tr>
                <td>MACD Level (12, 26)</td>
                <td>{technicalData.oscillators.MACD.macd[technicalData.oscillators.MACD.macd.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.Stochastic && (
              <>
                <tr>
                  <td>Stochastic %K (14, 3, 3)</td>
                  <td>{technicalData.oscillators.Stochastic.slowk[technicalData.oscillators.Stochastic.slowk.length - 1]?.toFixed(2)}</td>
                </tr>
                <tr>
                  <td>Stochastic %D (14, 3, 3)</td>
                  <td>{technicalData.oscillators.Stochastic.slowd[technicalData.oscillators.Stochastic.slowd.length - 1]?.toFixed(2)}</td>
                </tr>
              </>
            )}
            {technicalData.oscillators?.CCI && (
              <tr>
                <td>CCI (20)</td>
                <td>{technicalData.oscillators.CCI[technicalData.oscillators.CCI.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.ADX && (
              <tr>
                <td>ADX (14)</td>
                <td>{technicalData.oscillators.ADX[technicalData.oscillators.ADX.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.['Williams%R'] && (
              <tr>
                <td>Williams Percent Range (14)</td>
                <td>{technicalData.oscillators['Williams%R'][technicalData.oscillators['Williams%R'].length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.AO && (
              <tr>
                <td>Awesome Oscillator</td>
                <td>{technicalData.oscillators.AO[technicalData.oscillators.AO.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.Momentum && (
              <tr>
                <td>Momentum (10)</td>
                <td>{technicalData.oscillators.Momentum[technicalData.oscillators.Momentum.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.StochRSI && (
              <>
                <tr>
                  <td>Stochastic RSI Fast %K (3, 3, 14, 14)</td>
                  <td>{technicalData.oscillators.StochRSI.fastk[technicalData.oscillators.StochRSI.fastk.length - 1]?.toFixed(2)}</td>
                </tr>
                <tr>
                  <td>Stochastic RSI Fast %D (3, 3, 14, 14)</td>
                  <td>{technicalData.oscillators.StochRSI.fastd[technicalData.oscillators.StochRSI.fastd.length - 1]?.toFixed(2)}</td>
                </tr>
              </>
            )}
            {technicalData.oscillators?.BullBearPower && (
              <tr>
                <td>Bull Bear Power</td>
                <td>{technicalData.oscillators.BullBearPower[technicalData.oscillators.BullBearPower.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.oscillators?.UltimateOscillator && (
              <tr>
                <td>Ultimate Oscillator (7, 14, 28)</td>
                <td>{technicalData.oscillators.UltimateOscillator[technicalData.oscillators.UltimateOscillator.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="pivots-section">
        <h3>Pivots</h3>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {technicalData.pivots?.Classic && (
              <tr>
                <td>Classic</td>
                <td>{technicalData.pivots.Classic[technicalData.pivots.Classic.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.pivots?.Fibonacci && (
              <tr>
                <td>Fibonacci</td>
                <td>{technicalData.pivots.Fibonacci[technicalData.pivots.Fibonacci.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.pivots?.Camarilla && (
              <tr>
                <td>Camarilla</td>
                <td>{technicalData.pivots.Camarilla[technicalData.pivots.Camarilla.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.pivots?.Woodie && (
              <tr>
                <td>Woodie</td>
                <td>{technicalData.pivots.Woodie[technicalData.pivots.Woodie.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
            {technicalData.pivots?.DM && (
              <tr>
                <td>DM</td>
                <td>{technicalData.pivots.DM[technicalData.pivots.DM.length - 1]?.toFixed(2)}</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Technicals;
