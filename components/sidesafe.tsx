import React, { useEffect, useState } from 'react'
import { Grid, Sun, MessageCircle, Bell, Calendar, MoreHorizontal, ExternalLink, Plus, DollarSign } from 'lucide-react'
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import Link from 'next/link'
import { LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer, XAxis, YAxis, Tooltip, BarChart, Bar, Area, AreaChart } from 'recharts'


interface WatchlistStock {
  symbol: string
  price: number
  change: number
  changePercent: number
  companyName: string
}

interface Stock {
  symbol: string
  price: number
  change: number
  changePercent: number
  companyName: string
  exchange: string
  industry: string
  lastUpdated: string
  previousClose: number
  open: number
  dayLow: number
  dayHigh: number
  volume: number
  avgVolume: number
  avgVolume10days: number
  marketCap: number
  high52Week: number
  low52Week: number
  peRatio: number
  forwardPE: number
  eps: number
  forwardEps: number
  dividend: number
  beta: number
  priceToBook: number
  debtToEquity: number
  returnOnEquity: number
  returnOnAssets: number
  profitMargins: number
  operatingMargins: number
  sector: string
  description: string
  earningsData?: Array<{
    quarter: string
    actual: number
    estimate: number
  }>
  dividendData?: {
    retainedEarnings: number
    payoutRatio: number
  }
  financialData?: {
    revenue: number[]
    netIncome: number[]
    margins: number[]
    quarters: string[]
  }
}

interface SidebarProps {
  currentStock?: Stock;
  onShowTechnicals: () => void;
}

const GaugeChart = ({ value, type, label }) => {
  const angle = -90 + (value * 180);
  
  return (
    <div className="relative w-full h-[120px] mb-8">
      <div className="absolute top-0 left-0 text-[#666] text-xs">{type}</div>
      
      <svg className="w-full h-full" viewBox="0 0 200 120">
        {/* Background circle */}
        <path
          d="M20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#2a2a2a"
          strokeWidth="6"
          strokeLinecap="round"
        />
        
        {/* Colored sections based on type */}
        {type === 'Technicals' ? (
          <>
            <path
              d="M20 100 A 80 80 0 0 1 100 100"
              fill="none"
              stroke="#ff4444"
              strokeWidth="6"
              strokeLinecap="round"
            />
            <path
              d="M100 100 A 80 80 0 0 1 180 100"
              fill="none"
              stroke="#00ff88"
              strokeWidth="6"
              strokeLinecap="round"
            />
          </>
        ) : (
          <>
            <path
              d="M20 100 A 80 80 0 0 1 100 100"
              fill="none"
              stroke="url(#gradientYellow)"
              strokeWidth="6"
              strokeLinecap="round"
            />
            <path
              d="M100 100 A 80 80 0 0 1 180 100"
              fill="none"
              stroke="#00ff88"
              strokeWidth="6"
              strokeLinecap="round"
            />
          </>
        )}
        
        {/* Gradient definition for analyst rating */}
        <defs>
          <linearGradient id="gradientYellow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ff4444" />
            <stop offset="50%" stopColor="#ffbb00" />
            <stop offset="100%" stopColor="#00ff88" />
          </linearGradient>
        </defs>
        
        {/* Pointer */}
        <g transform={`rotate(${angle}, 100, 100)`}>
          <line x1="100" y1="100" x2="100" y2="40" stroke="#ffffff" strokeWidth="2" />
          <circle cx="100" cy="100" r="8" fill="#1a1a1a" stroke="#ffffff" strokeWidth="2" />
        </g>
        
        {/* Labels */}
        <text x="20" y="115" fontSize="10" fill="#666">Strong sell</text>
        <text x="90" y="115" fontSize="10" fill="#666">Neutral</text>
        <text x="155" y="115" fontSize="10" fill="#666">Strong buy</text>
      </svg>
      
      <div className="absolute top-[75px] left-0 right-0 text-center text-white text-sm font-medium">
        {label}
      </div>
    </div>
  );
};

const SeasonalsChart = () => {
  const data = [
    { date: 'Jan', y2023: -2, y2024: -3, y2025: -1 },
    { date: 'Apr', y2023: 1, y2024: -2, y2025: 0 },
    { date: 'Jul', y2023: 2, y2024: 1, y2025: null },
    { date: 'Oct', y2023: 3, y2024: 2, y2025: null }
  ];

  return (
    <div className="space-y-2 mb-8">
      <div className="text-[#666] text-xs">Seasonals</div>
      <ResponsiveContainer width="100%" height={150}>
        <LineChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
          <XAxis 
            dataKey="date" 
            stroke="#666" 
            fontSize={10}
            tickLine={false}
            axisLine={{ stroke: '#2a2a2a' }}
          />
          <YAxis 
            stroke="#666" 
            fontSize={10}
            tickLine={false}
            axisLine={false}
            domain={[-4, 4]}
          />
          <Line 
            type="monotone" 
            dataKey="y2025" 
            stroke="#4444ff" 
            dot={false}
            strokeWidth={1}
          />
          <Line 
            type="monotone" 
            dataKey="y2024" 
            stroke="#ff4444" 
            dot={false}
            strokeWidth={1}
          />
          <Line 
            type="monotone" 
            dataKey="y2023" 
            stroke="#aa44ff" 
            dot={false}
            strokeWidth={1}
          />
          <Tooltip 
            contentStyle={{ background: '#1a1a1a', border: '1px solid #2a2a2a' }}
            labelStyle={{ color: '#666' }}
            itemStyle={{ color: '#fff' }}
          />
        </LineChart>
      </ResponsiveContainer>
      <Button 
        variant="ghost" 
        size="sm" 
        className="w-full text-xs text-[#666] hover:text-white"
      >
        More seasonals
      </Button>
    </div>
  );
};

const TechnicalSection = ({ onShowTechnicals }) => {
  return (
    <div className="space-y-6">
      <div>
        <GaugeChart 
          value={0.3} 
          type="Technicals"
          label="Sell"
        />
      </div>
      
      <div>
        <GaugeChart 
          value={0.8} 
          type="Analyst rating"
          label="Strong buy"
        />
      </div>
      
      <div className="flex justify-between items-center text-xs mt-4">
        <span className="text-white">1 year price target</span>
        <div>
          <span className="text-white mr-2">2,013.95</span>
          <span className="text-[#00ff88]">(21.91%)</span>
        </div>
      </div>
      
      <Button 
        variant="ghost" 
        size="sm" 
        className="w-full text-xs text-[#666] hover:text-white"
        onClick={onShowTechnicals}  // Add this onClick handler
      >
        See forecast
      </Button>
      <Button 
        variant="ghost" 
        size="sm" 
        className="w-full text-xs text-[#666] hover:text-white"
        onClick={onShowTechnicals}  // Add this onClick handler
      >
        More technicals
      </Button>
    </div>
  );
};

export function Sidebar({ currentStock = {} as Stock, onShowTechnicals }: SidebarProps) {
  const [stockDetails, setStockDetails] = useState<Stock | null>(null);
  const [watchlist, setWatchlist] = useState<WatchlistStock[]>([]);
  const [newSymbol, setNewSymbol] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [activeFinancialView, setActiveFinancialView] = useState('income') // 'income', 'balance', 'cashflow'
  const [timeframe, setTimeframe] = useState('quarterly') // 'quarterly', 'annual'
  const [expandedSection, setExpandedSection] = useState('')


  useEffect(() => {
    const fetchStockDetails = async () => {
      try {
        if (!currentStock?.symbol) return;
        const response = await fetch(`http://localhost:5000/fetch_stock_details?symbol=${currentStock.symbol}`);
        const data = await response.json();
        if (!response.ok) throw new Error(data.error);
        setStockDetails(data);
      } catch (error) {
        console.error('Error fetching stock details:', error);
      }
    };

    if (currentStock?.symbol) {
      fetchStockDetails();
    }
  }, [currentStock?.symbol]);

  useEffect(() => {
    const fetchWatchlistData = async () => {
      if (watchlist.length === 0) return;
      try {
        const symbols = watchlist.map(stock => stock.symbol).join(',');
        const response = await fetch(`http://localhost:5000/fetch_multiple_stocks?symbols=${symbols}`);
        const data = await response.json();
        if (!response.ok) throw new Error(data.error);
        
        // Merge new data with existing watchlist
        setWatchlist(prevWatchlist => {
          return prevWatchlist.map(prevStock => {
            const updatedStock = data.find((s: WatchlistStock) => s.symbol === prevStock.symbol);
            return updatedStock ? { ...prevStock, ...updatedStock } : prevStock;
          });
        });
      } catch (error) {
        console.error('Error fetching watchlist:', error);
      }
    };

    const interval = setInterval(fetchWatchlistData, 10000); // Update every 10 seconds
    fetchWatchlistData(); // Initial fetch

    return () => clearInterval(interval);
  }, [watchlist]); // Changed dependency to just watchlist

  const addToWatchlist = async () => {
    if (!newSymbol) return;
    
    // Clear previous error
    setError(null);

    // Check for duplicate
    if (watchlist.some(stock => stock.symbol === newSymbol)) {
      setError(`${newSymbol} is already in your watchlist`);
      setNewSymbol('');
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/fetch_stock_details?symbol=${newSymbol}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);

      const newStock: WatchlistStock = {
        symbol: data.symbol,
        price: data.price,
        change: data.change,
        changePercent: data.changePercent,
        companyName: data.companyName,
      };

      setWatchlist(prev => [...prev, newStock]);
      setNewSymbol('');
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      setError('Failed to add stock to watchlist');
    }
  };

  const removeFromWatchlist = (symbol: string) => {
    setWatchlist(prev => prev.filter(stock => stock.symbol !== symbol));
  };

  // Use stockDetails if available, otherwise fall back to currentStock
  const displayStock = stockDetails || currentStock;

  // Sample earnings data
  const earningsData = [
    { quarter: 'Q3 23', actual: 21, estimate: null },
    { quarter: 'Q4 23', actual: 28, estimate: null },
    { quarter: 'Q1 24', actual: 24, estimate: null },
    { quarter: 'Q2 24', actual: 26, estimate: null },
    { quarter: 'Q3 24', actual: null, estimate: 23 },
  ]

  // Sample dividend data for pie chart
  const dividendData = [
    { name: 'Earnings Retained', value: 78.57 },
    { name: 'Payout Ratio', value: 21.43 }
  ]

  // Sample seasonality data
  const seasonalData = [
    { month: 'Jan', value2023: -2, value2024: -1, value2025: -3 },
    { month: 'Apr', value2023: 1, value2024: 2, value2025: null },
    { month: 'Jul', value2023: 3, value2024: 1, value2025: null },
    { month: 'Oct', value2023: 2, value2024: -1, value2025: null }
  ]

  // Sample financial data
  const financialData = {
    revenue: [1050, 1150, 1200, 1400, 1300],
    netIncome: [350, 400, 380, 450, 420],
    margins: [14.5, 14.2, 14.8, 14.3, 14.6],
    quarters: ['Q2 23', 'Q3 23', 'Q4 23', 'Q1 24', 'Q2 24']
  }

  // Sample technicals data
  const technicalsData = {
    indicators: [
      { name: 'RSI', value: 35 },
      { name: 'MACD', value: -2 },
      { name: 'MA(50)', value: 1645 },
      { name: 'MA(200)', value: 1630 }
    ],
    rating: 'Sell'
  }

  // Sample volatility data
  const volatilityData = Array.from({ length: 20 }, (_, i) => ({
    strike: 800 + i * 100,
    value: 50 - Math.cos(i / 3) * 25
  }))

  const COLORS = ['#2a2a2a', '#00ff88']

  const renderCharts = () => (
    <div className="space-y-6 p-4">
      {/* Earnings Chart */}
      <div>
        <div className="text-[#666] text-xs mb-2">Earnings</div>
        <ResponsiveContainer width="100%" height={120}>
          <LineChart data={earningsData}>
            <XAxis dataKey="quarter" stroke="#666" fontSize={10} />
            <YAxis stroke="#666" fontSize={10} />
            <Line 
              type="monotone" 
              dataKey="actual" 
              stroke="#00ff88" 
              dot={{ fill: '#00ff88' }}
            />
            <Line 
              type="monotone" 
              dataKey="estimate" 
              stroke="#666" 
              strokeDasharray="3 3"
              dot={{ fill: '#666' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Dividend Pie Chart */}
      <div>
        <div className="text-[#666] text-xs mb-2">Dividend Distribution</div>
        <ResponsiveContainer width="100%" height={120}>
          <PieChart>
            <Pie
              data={dividendData}
              cx="50%"
              cy="50%"
              innerRadius={25}
              outerRadius={40}
              paddingAngle={5}
              dataKey="value"
            >
              {dividendData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="text-center text-xs text-[#666] mt-2">
          Payout ratio (TTM): 21.43%
        </div>
      </div>

      {/* Seasonality Chart */}
      <div>
        <div className="text-[#666] text-xs mb-2">Seasonals</div>
        <ResponsiveContainer width="100%" height={120}>
          <LineChart data={seasonalData}>
            <XAxis dataKey="month" stroke="#666" fontSize={10} />
            <YAxis stroke="#666" fontSize={10} />
            <Line 
              type="monotone" 
              dataKey="value2023" 
              stroke="#ff4444" 
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="value2024" 
              stroke="#00ff88" 
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="value2025" 
              stroke="#4444ff" 
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Technical Indicator Gauge */}
      <div>
        <div className="text-[#666] text-xs mb-2">Technical Rating</div>
        <div className="h-[60px] relative">
          <div className="absolute inset-0 bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 rounded-full h-2" />
          <div className="absolute left-1/3 top-0 w-0.5 h-4 bg-white transform -translate-x-1/2" />
        </div>
        <div className="text-center text-xs text-[#666] mt-2">
          Sell
        </div>
      </div>
    </div>
  )

  const renderFinancialCharts = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div className="space-x-2">
          <Button
            variant={activeFinancialView === 'income' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveFinancialView('income')}
            className="text-xs"
          >
            Income
          </Button>
          <Button
            variant={activeFinancialView === 'balance' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveFinancialView('balance')}
            className="text-xs"
          >
            Balance Sheet
          </Button>
          <Button
            variant={activeFinancialView === 'cashflow' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveFinancialView('cashflow')}
            className="text-xs"
          >
            Cash Flow
          </Button>
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant={timeframe === 'quarterly' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setTimeframe('quarterly')}
            className="text-xs"
          >
            Q
          </Button>
          <Button
            variant={timeframe === 'annual' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setTimeframe('annual')}
            className="text-xs"
          >
            A
          </Button>
        </div>
      </div>

      <div className="h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={financialData.quarters.map((q, i) => ({
            quarter: q,
            revenue: financialData.revenue[i],
            netIncome: financialData.netIncome[i],
            margin: financialData.margins[i]
          }))}>
            <XAxis dataKey="quarter" stroke="#666" fontSize={10} />
            <YAxis yAxisId="left" stroke="#666" fontSize={10} />
            <YAxis yAxisId="right" orientation="right" stroke="#666" fontSize={10} />
            <Tooltip />
            <Bar yAxisId="left" dataKey="revenue" fill="#4444ff" />
            <Bar yAxisId="left" dataKey="netIncome" fill="#00ff88" />
            <Line yAxisId="right" type="monotone" dataKey="margin" stroke="#ff8800" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <Button 
        variant="ghost" 
        size="sm" 
        className="w-full text-xs text-[#666] hover:text-white"
        onClick={() => setExpandedSection('financials')}
      >
        More financials
      </Button>
    </div>
  )

  const renderTechnicals = () => (
    <div className="space-y-4">
      <div className="text-[#666] text-xs">Technicals</div>
      
      {/* Technical Gauge */}
      <div className="relative h-[60px]">
        <div className="absolute inset-x-0 top-1/2 h-2 bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 rounded-full" />
        <div className="absolute left-1/3 top-1/2 -mt-3 w-0.5 h-6 bg-white transform -translate-x-1/2" />
        <div className="absolute top-0 left-0 w-full text-center text-xs text-white">
          {technicalsData.rating}
        </div>
      </div>

      {/* Technical Indicators */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        {technicalsData.indicators.map(indicator => (
          <div key={indicator.name}>
            <span className="text-[#666]">{indicator.name}:</span>
            <span className="text-white ml-2">{indicator.value}</span>
          </div>
        ))}
      </div>

      <Button 
        variant="ghost" 
        size="sm" 
        className="w-full text-xs text-[#666] hover:text-white"
        onClick={() => setExpandedSection('technicals')}
      >
        More technicals
      </Button>
    </div>
  )

  const renderVolatilityCurve = () => (
    <div className="space-y-4">
      <div className="text-[#666] text-xs">Volatility Curve (42 days)</div>
      
      <ResponsiveContainer width="100%" height={120}>
        <AreaChart data={volatilityData}>
          <Area type="monotone" dataKey="value" stroke="#4444ff" fill="#4444ff20" />
          <XAxis dataKey="strike" stroke="#666" fontSize={10} />
          <YAxis stroke="#666" fontSize={10} domain={[0, 100]} />
        </AreaChart>
      </ResponsiveContainer>

      <Button 
        variant="ghost" 
        size="sm" 
        className="w-full text-xs text-[#666] hover:text-white"
        onClick={() => setExpandedSection('options')}
      >
        More on options
      </Button>
    </div>
  )

  return (
    <div className="h-full overflow-hidden flex flex-col bg-[#1a1a1a] border-l border-[#2a2a2a]">
      {/* Top Icons - Fixed */}
      <div className="p-2 border-b border-[#2a2a2a] flex justify-end space-x-1">
        <Link href="/watchlist">
          <Button 
          variant="ghost" 
          size="icon" 
          className="text-[#666] hover:text-white hover:bg-[#2a2a2a]"
          title="Watchlist"
          >
          <Grid className="h-4 w-4" />
          </Button>
        </Link>
        <Link href="/ideas">
          <Button 
          variant="ghost" 
          size="icon" 
          className="text-[#666] hover:text-white hover:bg-[#2a2a2a]"
          title="Ideas"
          >
          <Sun className="h-4 w-4" />
          </Button>
        </Link>
        <Link href="/chat">
          <Button 
          variant="ghost" 
          size="icon" 
          className="text-[#666] hover:text-white hover:bg-[#2a2a2a]"
          title="Chat"
          >
          <MessageCircle className="h-4 w-4" />
          </Button>
        </Link>
        <Link href="/screener">
          <Button 
          variant="ghost" 
          size="icon" 
          className="text-[#666] hover:text-white hover:bg-[#2a2a2a]"
          title="Alerts"
          >
          <Bell className="h-4 w-4" />
          </Button>
        </Link>
        <Link href="/financial">
          <Button 
          variant="ghost" 
          size="icon" 
          className="text-[#666] hover:text-white hover:bg-[#2a2a2a]"
          title="Financial"
          
          >
            <DollarSign className="h-4 w-4" />
          </Button>
          
          
        </Link>

        
        </div>

        {/* Watchlist Section - Fixed */}
        <div className="p-4 border-b border-[#2a2a2a]">
          <div className="flex items-center gap-2 mb-4">

          <Input
            value={newSymbol}
            onChange={(e) => setNewSymbol(e.target.value.toUpperCase())}
            placeholder="Add symbol..."
            className="bg-[#2a2a2a] border-none text-white"
          />
          <Button
            onClick={addToWatchlist}
            variant="ghost"
            size="icon"
            className="text-[#666] hover:text-white hover:bg-[#2a2a2a]"
          >
            <Plus className="h-4 w-4" />
          </Button>
          </div>

          <div className="grid grid-cols-[1fr_auto_auto] gap-4 text-xs">
          <div className="text-[#666]">Symbol</div>
          <div className="text-[#666] text-right">Last</div>
          <div className="text-[#666] text-right">Chg%</div>
            {watchlist.map((stock) => (
            <React.Fragment key={stock.symbol}>
              <div className="text-white flex items-center justify-between">
              <div className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-blue-500 mr-2" />
                {stock.symbol}
              </div>
              <Button
                onClick={() => removeFromWatchlist(stock.symbol)}
                variant="ghost"
                size="icon"
                className="h-4 w-4 text-[#666] hover:text-red-500"
              >
                ×
              </Button>
              </div>
              <div className="text-white text-right font-mono">
              {stock.price.toLocaleString()}
              </div>
                <div className={`text-right font-mono ${stock.changePercent >= 0 ? 'text-[#00ff88]' : 'text-[#ff4444]'}`}>
                {stock.changePercent > 0 ? '+' : ''}{typeof stock.changePercent === 'number' ? stock.changePercent.toFixed(2) : '0.00'}%
                </div>
            </React.Fragment>
            ))}
            </div>
          </div>

          {/* Stock Details Section - Scrollable */}
            <div className="flex-1 overflow-y-auto min-h-0 custom-scrollbar">
            <div className="p-4">
            <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="h-2 w-2 rounded-full bg-yellow-500" />
              <span className="text-white font-semibold">{displayStock?.symbol || '-'}</span>
            </div>
            <div className="flex space-x-1">
              <Button variant="ghost" size="icon" className="h-6 w-6 text-[#666] hover:text-white hover:bg-[#2a2a2a]">
                <Grid className="h-3 w-3" />
              </Button>
              <Button variant="ghost" size="icon" className="h-6 w-6 text-[#666] hover:text-white hover:bg-[#2a2a2a]">
                <ExternalLink className="h-3 w-3" />
              </Button>
              <Button variant="ghost" size="icon" className="h-6 w-6 text-[#666] hover:text-white hover:bg-[#2a2a2a]">
                <MoreHorizontal className="h-3 w-3" />
              </Button>
            </div>
          </div>
          
          <div>
            <div className="text-[#666] text-xs">{displayStock?.companyName || '-'} • {displayStock?.exchange || '-'}</div>
            <div className="text-[#666] text-xs">{displayStock?.industry || '-'}</div>
          </div>

            <div>
            <div className="text-white text-2xl font-mono">
              {displayStock?.price ? displayStock.price.toLocaleString() : '-'} 
              <span className="text-xs text-[#666]">INR</span>
            </div>
            <div className={`font-mono ${displayStock?.change && displayStock.change >= 0 ? 'text-[#00ff88]' : 'text-[#ff4444]'}`}>
              {displayStock?.change !== undefined && displayStock?.changePercent !== undefined ? (
              <>
                {displayStock.change > 0 ? '+' : ''}
                {typeof displayStock.change === 'number' ? displayStock.change.toFixed(2) : displayStock.change} {typeof displayStock.changePercent === 'number' ? displayStock.changePercent.toFixed(2) : displayStock.changePercent}%
              </>
              ) : '-'}
            </div>
            </div>

          
            {stockDetails && (
            <>
              <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <div className="text-[#666]">Previous Close</div>
                <div className="text-white">{typeof stockDetails.previousClose === 'number' ? stockDetails.previousClose.toLocaleString() : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Open</div>
                <div className="text-white">{typeof stockDetails.open === 'number' ? stockDetails.open.toLocaleString() : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Day Range</div>
                <div className="text-white">
                {typeof stockDetails.dayLow === 'number' && typeof stockDetails.dayHigh === 'number' 
                  ? `${stockDetails.dayLow.toLocaleString()} - ${stockDetails.dayHigh.toLocaleString()}` 
                  : '-'}
                </div>
              </div>
              <div>
                <div className="text-[#666]">52 Week Range</div>
                <div className="text-white">
                {typeof stockDetails.low52Week === 'number' && typeof stockDetails.high52Week === 'number'
                  ? `${stockDetails.low52Week.toLocaleString()} - ${stockDetails.high52Week.toLocaleString()}`
                  : '-'}
                </div>
              </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <div className="text-[#666]">Volume</div>
                <div className="text-white">{typeof stockDetails.volume === 'number' ? stockDetails.volume.toLocaleString() : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Avg. Volume</div>
                <div className="text-white">{typeof stockDetails.avgVolume === 'number' ? stockDetails.avgVolume.toLocaleString() : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">10-Day Avg. Volume</div>
                <div className="text-white">{typeof stockDetails.avgVolume10days === 'number' ? stockDetails.avgVolume10days.toLocaleString() : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Market Cap</div>
                <div className="text-white">{typeof stockDetails.marketCap === 'number' ? `${(stockDetails.marketCap / 1e9).toFixed(2)}B` : '-'}</div>
              </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <div className="text-[#666]">Beta</div>
                <div className="text-white">{typeof stockDetails.beta === 'number' ? stockDetails.beta.toFixed(2) : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Debt/Equity</div>
                <div className="text-white">{typeof stockDetails.debtToEquity === 'number' ? stockDetails.debtToEquity.toFixed(2) : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">P/E Ratio (TTM)</div>
                <div className="text-white">{typeof stockDetails.peRatio === 'number' ? stockDetails.peRatio.toFixed(2) : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Forward P/E</div>
                <div className="text-white">{typeof stockDetails.forwardPE === 'number' ? stockDetails.forwardPE.toFixed(2) : '-'}</div>
              </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <div className="text-[#666]">EPS (TTM)</div>
                <div className="text-white">{typeof stockDetails.eps === 'number' ? stockDetails.eps.toFixed(2) : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Forward EPS</div>
                <div className="text-white">{typeof stockDetails.forwardEps === 'number' ? stockDetails.forwardEps.toFixed(2) : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Price/Book</div>
                <div className="text-white">{typeof stockDetails.priceToBook === 'number' ? stockDetails.priceToBook.toFixed(2) : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Dividend Yield</div>
                <div className="text-white">{typeof stockDetails.dividend === 'number' ? `${(stockDetails.dividend * 100).toFixed(2)}%` : '-'}</div>
              </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <div className="text-[#666]">ROE</div>
                <div className="text-white">{typeof stockDetails.returnOnEquity === 'number' ? `${(stockDetails.returnOnEquity * 100).toFixed(2)}%` : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">ROA</div>
                <div className="text-white">{typeof stockDetails.returnOnAssets === 'number' ? `${(stockDetails.returnOnAssets * 100).toFixed(2)}%` : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Profit Margin</div>
                <div className="text-white">{typeof stockDetails.profitMargins === 'number' ? `${(stockDetails.profitMargins * 100).toFixed(2)}%` : '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Operating Margin</div>
                <div className="text-white">{typeof stockDetails.operatingMargins === 'number' ? `${(stockDetails.operatingMargins * 100).toFixed(2)}%` : '-'}</div>
              </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <div className="text-[#666]">Sector</div>
                <div className="text-white">{stockDetails.sector || '-'}</div>
              </div>
              <div>
                <div className="text-[#666]">Industry</div>
                <div className="text-white">{stockDetails.industry || '-'}</div>
              </div>
              </div>

              <div className="text-xs">
              <div className="text-[#666]">Description</div>
              <div className="text-white text-sm mt-1">{stockDetails.description || '-'}</div>
              </div>

              {/* New charts section */}
              {stockDetails && renderCharts()}
              {renderFinancialCharts()}
              {renderTechnicals()}
              {renderVolatilityCurve()}
              <SeasonalsChart />
              <TechnicalSection onShowTechnicals={onShowTechnicals} />
            </>
            )}

          <div className="flex items-center justify-between text-xs">
            <span className="text-[#666]">Market closed</span>
            <div className="flex items-center space-x-2">
              <span className="text-[#666]">
                {displayStock?.lastUpdated ? `Last updated at ${displayStock.lastUpdated}` : '-'}
              </span>
              <Button variant="ghost" size="icon" className="h-6 w-6 text-[#666] hover:text-white hover:bg-[#2a2a2a]">
                <Calendar className="h-3 w-3" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
);
}
