interface SymbolSelectProps {
  onSymbolChange: (symbol: string) => void;
}

export const SymbolSelect: React.FC<SymbolSelectProps> = ({ onSymbolChange }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.toUpperCase();
    onSymbolChange(value);
  };

  return (
    <input
      type="text"
      onChange={handleChange}
      placeholder="Enter symbol..."
      defaultValue="AAPL"
      className="bg-[#1e1e1e] text-white px-3 py-1 rounded border border-[#2a2a2a]"
    />
  );
}; 