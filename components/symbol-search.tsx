import React, { useState, useEffect } from 'react';
import { Command } from 'cmdk';

interface SymbolSearchProps {
  isOpen: boolean;
  onClose: () => void;
  onSymbolSelect: (symbol: string) => void;
}

export const SymbolSearch: React.FC<SymbolSearchProps> = ({ isOpen, onClose, onSymbolSelect }) => {
  const [search, setSearch] = useState('');
  const [results, setResults] = useState<Array<{ symbol: string, name: string, exchange: string }>>([]);

  useEffect(() => {
    if (search.length > 1) {
      fetch(`http://localhost:5000/get_stock_suggestions?query=${encodeURIComponent(search)}`)
        .then(res => res.json())
        .then(data => {
          console.log('Search results:', data); // Debug log
          setResults(data);
        })
        .catch(err => console.error('Search error:', err));
    } else {
      setResults([]);
    }
  }, [search]);

  return (
    <Command.Dialog
      open={isOpen}
      onOpenChange={onClose}
      className="fixed inset-0 z-50 flex items-start justify-center pt-20"
      overlayClassName="fixed inset-0 bg-black/50"
    >
      <Command className="w-[640px] bg-[#1E1E1E] rounded-lg border border-[#2a2e39] shadow-2xl overflow-hidden">
        <Command.Input 
          value={search}
          onValueChange={setSearch}
          className="w-full px-4 py-3 bg-transparent text-white border-b border-[#2a2e39] outline-none"
          placeholder="Search symbol..."
          autoFocus
        />
        <Command.List className="max-h-[400px] overflow-auto p-2">
          {results.length > 0 ? (
            results.map((result) => (
              <Command.Item
                key={`${result.symbol}-${result.exchange}`}
                onSelect={() => {
                  onSymbolSelect(result.fullSymbol);  // Use the full symbol with exchange
                  onClose();
                }}
                className="px-4 py-2 hover:bg-[#2a2e39] cursor-pointer flex items-center justify-between rounded"
              >
                <span className="font-bold text-white">{result.symbol}</span>
                <span className="text-gray-400">{result.name}</span>
              </Command.Item>
            ))
          ) : (
            <div className="px-4 py-2 text-gray-400">
              {search.length > 1 ? 'No results found' : 'Start typing to search...'}
            </div>
          )}
        </Command.List>
      </Command>
    </Command.Dialog>
  );
};
