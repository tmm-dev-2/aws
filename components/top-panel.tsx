"use client"

import React, { useState, useEffect } from 'react'
import { ChevronDown } from 'lucide-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

interface LayoutOption {
  id: string;
  name: string;
  grid: string;
}

const layoutOptions: LayoutOption[] = [
  { id: 'single', name: 'Single View', grid: 'grid-cols-1 grid-rows-1' },
  { id: 'horizontal-2', name: '2 Charts Horizontal', grid: 'grid-cols-2 grid-rows-1' },
  { id: 'vertical-2', name: '2 Charts Vertical', grid: 'grid-cols-1 grid-rows-2' },
  { id: 'triple', name: '3 Charts', grid: 'grid-cols-2 grid-rows-2' },
  { id: 'quad', name: '4 Charts', grid: 'grid-cols-2 grid-rows-2' },
  { id: 'horizontal-3', name: '3 Charts Horizontal', grid: 'grid-cols-3 grid-rows-1' },
  { id: 'vertical-3', name: '3 Charts Vertical', grid: 'grid-cols-1 grid-rows-3' }
];

interface TopPanelProps {
  onSymbolChange: (symbol: string) => void
  onPeriodChange: (period: string) => void
  onStrategyChange: (strategy: string) => void
  selectedPeriod: string
  selectedStrategy: string
  currentStock: Stock
  onLayoutChange: (layout: string) => void;
  selectedLayout: string;
}

interface Stock {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  lastUpdated: string;
  companyName: string;
  exchange: string;
  industry: string;
}

const LayoutSelector = ({ selectedLayout, onLayoutChange }: { 
  selectedLayout: string, 
  onLayoutChange: (layout: string) => void 
}) => {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="flex items-center gap-2 p-2 bg-[#2a2e39] hover:bg-[#363c4e] rounded">
          <div className="w-4 h-4 grid grid-cols-2 gap-[1px]">
            {/* Show current layout icon based on selectedLayout */}
            {getLayoutIcon(selectedLayout)}
          </div>
          <ChevronDown className="w-4 h-4" />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Content className="bg-[#2a2e39] rounded-md shadow-lg p-1 z-50">
        <DropdownMenu.Group>
          {/* Single Chart */}
          <DropdownMenu.Item 
            className={`flex items-center gap-3 p-2 hover:bg-[#363c4e] rounded cursor-pointer ${
              selectedLayout === 'single' ? 'bg-[#363c4e]' : ''
            }`}
            onClick={() => onLayoutChange('single')}
          >
            <div className="w-4 h-4 border border-white rounded-sm"/>
            <span>Single Chart</span>
          </DropdownMenu.Item>

          {/* Horizontal 2 Charts */}
          <DropdownMenu.Item 
            className={`flex items-center gap-3 p-2 hover:bg-[#363c4e] rounded cursor-pointer ${
              selectedLayout === 'horizontal-2' ? 'bg-[#363c4e]' : ''
            }`}
            onClick={() => onLayoutChange('horizontal-2')}
          >
            <div className="w-4 h-4 flex">
              <div className="w-1/2 border border-white rounded-sm"/>
              <div className="w-1/2 border border-white rounded-sm"/>
            </div>
            <span>2 Charts Horizontal</span>
          </DropdownMenu.Item>

          {/* Add other layout options similarly */}
        </DropdownMenu.Group>
      </DropdownMenu.Content>
    </DropdownMenu.Root>
  );
};

// Helper function to get the current layout icon
const getLayoutIcon = (layout: string) => {
  switch (layout) {
    case 'single':
      return <div className="col-span-2 border border-white rounded-sm"/>;
    case 'horizontal-2':
      return (
        <>
          <div className="border border-white rounded-sm"/>
          <div className="border border-white rounded-sm"/>
        </>
      );
    // Add other layout icons
    default:
      return <div className="col-span-2 border border-white rounded-sm"/>;
  }
};

export const TopPanel: React.FC<TopPanelProps> = ({
  onSymbolChange,
  onPeriodChange,
  onStrategyChange,
  selectedPeriod,
  selectedStrategy,
  currentStock,
  onLayoutChange,
  selectedLayout
}) => {
  const [symbolInput, setSymbolInput] = useState(currentStock.symbol);

  const timeframes = [
    { value: '1d', label: '1 Day' },
    { value: '2d', label: '2 Days' },
    { value: '1w', label: '1 Week' },
    { value: '2w', label: '2 Weeks' },
    { value: '1m', label: '1 Month' },
    { value: '2m', label: '2 Months' },
    { value: '3m', label: '3 Months' },
    { value: '6m', label: '6 Months' },
    { value: '1y', label: '1 Year' },
    { value: '2y', label: '2 Years' }
  ];

  const strategies = [
    { value: 'none', label: 'None' },
    { value: 'double-hull-turbo-p1', label: 'Double Hull Turbo P1' },
    { value: 'kernel-regression-p1', label: 'Kernel regression P1' }
  ];

  const handleSymbolChange = async (newSymbol: string) => {
    const symbol = newSymbol.toUpperCase();
    onSymbolChange(symbol);
    
    // Dispatch custom event for chart update
    const event = new CustomEvent('symbolChange', { 
      detail: { 
        symbol,
        period: selectedPeriod 
      } 
    });
    window.dispatchEvent(event);
  };

  const handleTimeframeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newTimeframe = event.target.value;
    onPeriodChange(newTimeframe);
    
    // Dispatch period change event
    const customEvent = new CustomEvent('periodChange', { 
      detail: { 
        symbol: currentStock.symbol,
        period: newTimeframe 
      } 
    });
    window.dispatchEvent(customEvent);
  };

  const handleStrategyChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newStrategy = event.target.value;
    onStrategyChange(newStrategy);
    
    // Dispatch strategy change event
    const customEvent = new CustomEvent('strategyChange', { 
      detail: { 
        symbol: currentStock.symbol,
        period: selectedPeriod,
        strategy: newStrategy
      } 
    });
    window.dispatchEvent(customEvent);
  };

  const handleLayoutChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newLayout = event.target.value;
    onLayoutChange(newLayout);
  };

  return (
    <div className="flex items-center justify-center px-4 py-2 bg-[#1b1b1a] border-b border-gray-700">
      <div className="flex items-center space-x-4">
        <input
          type="text"
          placeholder="Enter symbol..."
          value={symbolInput}
          onChange={(e) => {
            setSymbolInput(e.target.value);
            handleSymbolChange(e.target.value);
          }}
          className="bg-[#2b2b2a] text-white px-4 py-2 rounded-md w-40"
        />
        <select 
          value={selectedPeriod} 
          onChange={handleTimeframeChange}
          className="bg-[#2b2b2a] text-white px-4 py-2 rounded-md w-32"
        >
          {timeframes.map((tf) => (
            <option key={tf.value} value={tf.value}>
              {tf.label}
            </option>
          ))}
        </select>
        <select 
          value={selectedStrategy} 
          onChange={handleStrategyChange}
          className="bg-[#2b2b2a] text-white px-4 py-2 rounded-md w-48"
        >
          {strategies.map((strategy) => (
            <option key={strategy.value} value={strategy.value}>
              {strategy.label}
            </option>
          ))}
        </select>
        <LayoutSelector selectedLayout={selectedLayout} onLayoutChange={onLayoutChange} />
      </div>
    </div>
  );
};