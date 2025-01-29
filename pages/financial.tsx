"use client"

import React, { useState } from 'react';
import { Sidebar } from '../components/sidebar';
import { Button } from "../components/ui/button";
import { BarChartIcon as ChartBarIcon, NewspaperIcon, PieChartIcon as ChartPieIcon, BarChart3Icon, LineChart, Search, Receipt, Wallet, ArrowDownUp } from 'lucide-react';
import '../app/globals.css';
import FinancialTable from '../components/financial-table';
import BS from '../components/BS';
import CashFlow from '../components/CashFlow';
import StatisticsTable from '../components/statistics';

type TabType = 'financial' | 'statistics' | 'analysis' | 'news' | 'chart';
type FinancialStatementType = 'income_statement' | 'balance_sheet' | 'cash_flow';

interface FinancialData {
  income_statement: any;
  balance_sheet: any;
  cash_flow: any;
  quarterly_financials: any;
  quarterly_balance_sheet: any;
  quarterly_cashflow: any;
  statistics: any
}

export default function FinancialPage() {
  const [activeTab, setActiveTab] = useState<TabType>('financial');
  const [searchQuery, setSearchQuery] = useState('');
  const [financialData, setFinancialData] = useState<FinancialData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isQuarterly, setIsQuarterly] = useState(false);
  const [activeStatement, setActiveStatement] = useState<FinancialStatementType>('income_statement');

  const fetchFinancialData = async (symbol: string) => {
    if (!symbol) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:5000/fetch_financials?symbol=${symbol}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch financial data');
      }
      
      const data = await response.json();
      setFinancialData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const fetchBalanceSheetData = async (symbol: string) => {
    if (!symbol) return;
  
    setLoading(true);
    setError(null);
  
    try {
      const response = await fetch(`http://localhost:5000/fetch_balance_sheet?symbol=${symbol}`);
  
      if (!response.ok) {
        throw new Error('Failed to fetch balance sheet data');
      }
  
      const data = await response.json();
      setFinancialData((prevData) => ({
        ...prevData,
        balance_sheet: data.balance_sheet,
      }));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const fetchCashFlowData = async (symbol: string) => {
    if (!symbol) return;
  
    setLoading(true);
    setError(null);
  
    try {
      const response = await fetch(`http://localhost:5000/fetch_cash_flow?symbol=${symbol}`);
  
      if (!response.ok) {
        throw new Error('Failed to fetch cash flow data');
      }
  
      const data = await response.json();
      setFinancialData((prevData) => ({
        ...prevData,
        cash_flow: data.cash_flow,
      }));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const fetchStatisticsData = async (symbol: string) => {
    if (!symbol) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:5000/fetch_statistics?symbol=${symbol}`);

      if (!response.ok) {
        throw new Error('Failed to fetch statistics data');
      }

      const data = await response.json();
      setFinancialData((prevData) => ({
        ...prevData,
        statistics: data.statistics,
      }));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchFinancialData(searchQuery);
    fetchBalanceSheetData(searchQuery);
    fetchCashFlowData(searchQuery);
    fetchStatisticsData(searchQuery);
  };

  return (
    <main className="flex h-screen text-white bg-[#1a1a1a]">
      {/* Main content first */}
      <div className="flex-1 flex flex-col">
        {/* Top Navigation Bar */}
        <div className="flex-shrink-0 border-b border-[#333333]">
            {/* Search Bar Section */}
            <form onSubmit={handleSearch} className="px-4 py-2 border-b border-[#333333]">
            <div className="relative max-w-md">
              <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-2 text-muted-foreground" />
              <input
              type="text"
              placeholder="Search Stocks, Symbols....."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-[#1a1a1a] rounded-md border border-[#333333] focus:outline-none focus:ring-1 focus:ring-blue-500 text-white placeholder-muted-foreground text-sm"
              />
            </div>
            </form>

          {/* Navigation Buttons */}
          <div className="flex items-center p-2 space-x-2">
            <Button
              variant={activeTab === 'financial' ? 'secondary' : 'ghost'}
              className={`flex items-center space-x-2 ${
                activeTab === 'financial' 
                  ? 'bg-secondary text-secondary-foreground' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
              }`}
              onClick={() => setActiveTab('financial')}
            >
              <ChartPieIcon className="h-4 w-4" />
              <span>Financial Data</span>
            </Button>

            <Button
              variant={activeTab === 'statistics' ? 'secondary' : 'ghost'}
              className={`flex items-center space-x-2 ${
                activeTab === 'statistics' 
                  ? 'bg-secondary text-secondary-foreground' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
              }`}
              onClick={() => setActiveTab('statistics')}
            >
              <BarChart3Icon className="h-4 w-4" />
              <span>Statistics</span>
            </Button>

            <Button
              variant={activeTab === 'analysis' ? 'secondary' : 'ghost'}
              className={`flex items-center space-x-2 ${
                activeTab === 'analysis' 
                  ? 'bg-secondary text-secondary-foreground' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
              }`}
              onClick={() => setActiveTab('analysis')}
            >
              <ChartBarIcon className="h-4 w-4" />
              <span>Analysis</span>
            </Button>

            <Button
              variant={activeTab === 'news' ? 'secondary' : 'ghost'}
              className={`flex items-center space-x-2 ${
                activeTab === 'news' 
                  ? 'bg-secondary text-secondary-foreground' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
              }`}
              onClick={() => setActiveTab('news')}
            >
              <NewspaperIcon className="h-4 w-4" />
              <span>News</span>
            </Button>

            <Button
              variant={activeTab === 'chart' ? 'secondary' : 'ghost'}
              className={`flex items-center space-x-2 ${
                activeTab === 'chart' 
                  ? 'bg-secondary text-secondary-foreground' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
              }`}
              onClick={() => setActiveTab('chart')}
            >
              <LineChart className="h-4 w-4" />
              <span>Chart</span>
            </Button>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 p-6 overflow-auto">
          <div className="text-white">
          {activeTab === 'financial' && (
            <div className="space-y-8">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">Financial Data</h2>
              <div className="space-x-2">
              <Button
                variant="outline"
                size="sm"
                className={`${!isQuarterly ? 'bg-secondary' : ''}`}
                onClick={() => setIsQuarterly(false)}
              >
                Annual
              </Button>
              <Button
                variant="outline"
                size="sm"
                className={`${isQuarterly ? 'bg-secondary' : ''}`}
                onClick={() => setIsQuarterly(true)}
              >
                Quarterly
              </Button>
              </div>
            </div>

            <div className="flex space-x-2 mb-6">
              <Button
              variant="outline"
              size="sm"
              className={`flex items-center space-x-2 px-4 py-1 text-sm ${
                activeStatement === 'income_statement' 
                ? 'bg-[#1a1a1a] text-white' 
                : 'bg-[#1a1a1a] text-gray-400 hover:text-white hover:bg-[#2a2a2a]'
              } border border-[#333333]`}
              onClick={() => setActiveStatement('income_statement')}
              >
              <Receipt className="h-4 w-4" />
              <span>Income Statement</span>
              </Button>
              <Button
              variant="outline"
              size="sm"
              className={`flex items-center space-x-2 px-4 py-1 text-sm ${
                activeStatement === 'balance_sheet' 
                ? 'bg-[#1a1a1a] text-white' 
                : 'bg-[#1a1a1a] text-gray-400 hover:text-white hover:bg-[#2a2a2a]'
              } border border-[#333333]`}
              onClick={() => setActiveStatement('balance_sheet')}
              >
              <Wallet className="h-4 w-4" />
              <span>Balance Sheet</span>
              </Button>
              <Button
              variant="outline"
              size="sm"
              className={`flex items-center space-x-2 px-4 py-1 text-sm ${
                activeStatement === 'cash_flow' 
                ? 'bg-[#1a1a1a] text-white' 
                : 'bg-[#1a1a1a] text-gray-400 hover:text-white hover:bg-[#2a2a2a]'
              } border border-[#333333]`}
              onClick={() => setActiveStatement('cash_flow')}
              >
              <ArrowDownUp className="h-4 w-4" />
              <span>Cash Flow</span>
              </Button>
            </div>
            
            <div className="bg-[#1a1a1a] rounded-lg p-6">
              {loading && <div className="text-center py-4">Loading...</div>}
              {error && <div className="text-red-500 text-center py-4">{error}</div>}
                {financialData && (
                  <>
                  {activeStatement === 'income_statement' && (
                    <FinancialTable 
                    title="Income Statement"
                    data={financialData.income_statement}
                    />
                  )}
                  {activeStatement === 'balance_sheet' && financialData?.balance_sheet && (
                    <div className="space-y-6">
                      <BS data={financialData.balance_sheet} />
                    </div>
                  )}
                  {activeStatement === 'cash_flow' && financialData.cash_flow && (
                    <div className="space-y-6">
                      <CashFlow data={financialData.cash_flow} />
                    </div>
                  )}
                  </>
                )}
            </div>
            </div>
          )}
            {activeTab === 'statistics' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold">Statistics</h2>
                <div className="bg-secondary rounded-lg p-6">
                  {loading && <div className="text-center py-4">Loading...</div>}
                  {error && <div className="text-red-500 text-center py-4">{error}</div>}
                  {financialData?.statistics && (
                    <StatisticsTable data={financialData.statistics} />
                  )}
                </div>
              </div>
            )}
            {activeTab === 'analysis' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold">Analysis</h2>
                <div className="bg-secondary rounded-lg p-6">
                  <div className="text-muted-foreground">Analysis content goes here</div>
                </div>
              </div>
            )}
            {activeTab === 'news' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold">News</h2>
                <div className="bg-secondary rounded-lg p-6">
                  <div className="text-muted-foreground">News content goes here</div>
                </div>
              </div>
            )}
            {activeTab === 'chart' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold">Chart</h2>
                <div className="bg-secondary rounded-lg p-6">
                  <div className="text-muted-foreground">Chart content goes here</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Sidebar last */}
        <div className="w-[350px] bg-[#1a1a1a] border-l border-[#333333]">
        <Sidebar />
      </div>
    </main>
  );
}
