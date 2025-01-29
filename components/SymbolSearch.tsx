import { useState, useEffect } from 'react';
import { Command } from 'cmdk';

interface SymbolSearchProps {
  isOpen: boolean;
  onClose: () => void;
  onSymbolSelect: (symbol: string) => void;
}

export const SymbolSearch = ({ isOpen, onClose, onSymbolSelect }: SymbolSearchProps) => {
  const [search, setSearch] = useState('');
  const [results, setResults] = useState<Array<{ symbol: string, name: string, exchange: string, fullSymbol: string }>>([]);

  useEffect(() => {
    const fetchSymbols = async () => {
      const response = await fetch(`http://localhost:5000/get_stock_suggestions?query=${encodeURIComponent(search)}`);
      const data = await response.json();
      console.log('Fetched data:', data);
      setResults(data);
    };

    if (search) {
      fetchSymbols();
    }
  }, [search]);

  return (
    <div className={`fixed inset-0 z-50 ${isOpen ? '' : 'hidden'}`}>
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[500px]">
        <Command className="w-full bg-[#1E1E1E] rounded-lg border border-[#2a2e39] shadow-xl overflow-hidden">
          <Command.Input 
            value={search}
            onValueChange={setSearch}
            className="w-full px-4 py-3 bg-transparent text-white border-b border-[#2a2e39] outline-none"
            placeholder="Search symbol..."
            autoFocus
          />
          <div className="max-h-[300px] overflow-auto">
            {results && results.length > 0 ? (
              results.map((result) => (
                <Command.Item
                  key={`${result.symbol}-${result.exchange}`}
                  onSelect={() => {
                    onSymbolSelect(result.fullSymbol || `${result.exchange}:${result.symbol}`);
                    onClose();
                  }}
                  className="px-4 py-2 hover:bg-[#2a2e39] cursor-pointer flex items-center justify-between"
                >
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-white">{result.symbol}</span>
                    <span className="text-xs text-gray-500">{result.exchange}</span>
                  </div>
                  <span className="text-gray-400">{result.name}</span>
                </Command.Item>
              ))
            ) : (
              <div className="px-4 py-2 text-gray-400">
                {search ? 'Type to search...' : 'Enter a symbol...'}
              </div>
            )}
          </div>
        </Command>
      </div>
    </div>
  );
};
