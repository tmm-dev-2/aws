import React, { useState } from 'react';

interface TopPanelProps {
  onSymbolChange: (symbol: string) => void;
  onPeriodChange: (period: string) => void;
  onStrategyChange: (strategy: string) => void;
  selectedPeriod: string;
  selectedStrategy: string;
}

const TopPanel: React.FC<TopPanelProps> = ({
  onSymbolChange,
  onPeriodChange,
  onStrategyChange,
  selectedPeriod,
  selectedStrategy
}) => {
  const [symbol, setSymbol] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (symbol.trim()) {
      onSymbolChange(symbol.trim().toUpperCase());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <div className="flex items-center gap-2 p-2 bg-[#131722]">
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Enter symbol..."
        className="bg-[#131722] text-white border border-[#2a2e39] rounded px-3 py-1 min-w-[200px] h-[32px] placeholder-gray-600"
      />
      
      <select 
        className="bg-[#2a2e39] text-white border-none rounded px-3 py-1 h-[32px] w-[60px] hover:bg-[#363c4e]"
        value={selectedPeriod}
        onChange={(e) => onPeriodChange(e.target.value)}
      >
        <option value="1d">1d</option>
        <option value="1h">1h</option>
        <option value="4h">4h</option>
        <option value="1w">1w</option>
        <option value="1m">1m</option>
        <option value="5m">5m</option>
        <option value="15m">15m</option>
        <option value="30m">30m</option>
        <option value="1M">1M</option>
      </select>

      <select 
        className="bg-[#2a2e39] text-white border-none rounded px-3 py-1 h-[32px] w-[200px] hover:bg-[#363c4e]"
        value={selectedStrategy}
        onChange={(e) => onStrategyChange(e.target.value)}
      >
        <option value="none">None</option>
        <option value="liquidations_schaff">Liquidations & Schaff Trend Cycle P1</option>
      </select>
    </div>
  );
};

export default TopPanel; 