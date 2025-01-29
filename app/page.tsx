"use client"

import { useState } from 'react';
import { Button } from "components/ui/button";
import { MainChart, MainChartContainer } from "components/main-chart";
import { Sidebar } from "components/sidebar";
import { DrawingTools } from "components/drawing-tools";
import { TopPanel } from "components/top-panel";
import { LeftSidePane } from "components/left-side-pane";
import dynamic from 'next/dynamic'
import LoginPage from 'components/auth/LoginPage'; // Import the LoginPage component
import { X } from 'lucide-react'; // Import the X icon
import Technicals from "../components/Technicals";
import { Resizable } from 're-resizable'; // Import Resizable component
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';
import { TradingView } from '../components/tmm-chart'





const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET!,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID!,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID!
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const ScriptEditor = dynamic(
  () => import('../components/ScriptEditor'),
  { ssr: false }
)

interface Stock {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  lastUpdated: string;
  companyName: string;
  exchange: string;
  industry: string;
  previousClose?: number;
  open?: number;
  dayLow?: number;
  dayHigh?: number;
  volume?: number;
  marketCap?: number;
  peRatio?: number;
}

interface CandleData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface User {
  googleId: string;
  imageUrl: string;
  email: string;
  name: string;
  givenName: string;
  familyName: string;
}

export default function Home() {
  const [selectedPeriod, setSelectedPeriod] = useState('1d');
  const [selectedStrategy, setSelectedStrategy] = useState('none');
  const [candleData, setCandleData] = useState<CandleData[]>([]);
  const [currentStock, setCurrentStock] = useState<Stock>({
    symbol: '',
    price: 0,
    change: 0,
    changePercent: 0,
    lastUpdated: '',
    companyName: '',
    exchange: '',
    industry: ''
  });
  const [isLoginPageActive, setIsLoginPageActive] = useState(false); // State for login page
  const [loggedInUser, setLoggedInUser] = useState<User | null>(null);
  const [showTechnicalsOverlay, setShowTechnicalsOverlay] = useState(false); // Add new state for technicals overlay
  const [lastChartData, setLastChartData] = useState<{symbol: string, period: string} | null>(null);
  const [selectedLayout, setSelectedLayout] = useState('single');
  const [symbols, setSymbols] = useState(['BTCUSDT']);

  const fetchData = async (symbol: string, period: string) => {
    if (!symbol) return;
    
    try {
      console.log(`Fetching data for ${symbol} with timeframe ${period}`);
      const response = await fetch(
        `http://localhost:5000/fetch_candles?symbol=${symbol}&timeframe=${period}`,
        {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Server error:', errorData.error || 'Unknown error'); // Add fallback message
        return;
      }

      const rawData = await response.json();
      console.log(`Received ${rawData.length} candles for ${period} timeframe`);
      
      const formattedData = rawData
        .map((d: any) => {
          if (!d.time || typeof d.time !== 'number' || isNaN(d.time)) {
            console.error('Invalid time value:', d.time);
            return null;
          }

          return {
            time: d.time,
            open: Number(d.open),
            high: Number(d.high),
            low: Number(d.low),
            close: Number(d.close),
            volume: Number(d.volume)
          };
        })
        .filter((d: any) => d !== null);

      console.log(`Formatted ${formattedData.length} candles`);
      setCandleData(formattedData);
      
      if (formattedData.length > 0) {
        const lastData = formattedData[formattedData.length - 1];
        const changePercent = lastData.open !== 0 
          ? ((lastData.close - lastData.open) / lastData.open) * 100 
          : 0;
          
        setCurrentStock(prev => ({
          ...prev,
          symbol: symbol,
          price: lastData.close,
          change: lastData.close - lastData.open,
          changePercent: changePercent,
          lastUpdated: new Date(lastData.time * 1000).toLocaleTimeString(),
        }));

        // Save to Firebase after successful fetch
        const db = getFirestore();
        const lastChartRef = doc(db, 'userCharts', loggedInUser?.googleId || 'default');
        await setDoc(lastChartRef, {
          symbol,
          period,
          timestamp: new Date()
        });
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleChartClick = async () => {
    // Close all overlay states
    setIsLoginPageActive(false);
    setShowTechnicalsOverlay(false);
    // Add any other overlay/page states here as needed
  
    try {
      const lastChartRef = doc(db, 'userCharts', loggedInUser?.googleId || 'default');
      const docSnap = await getDoc(lastChartRef);
      
      console.log('Retrieved Firebase data:', docSnap.data());
      
      if (docSnap.exists()) {
        const data = docSnap.data();
        console.log('Setting chart data:', data);
        
        // Update period first
        setSelectedPeriod(data.period);
        console.log('Period set to:', data.period);
        
        // Update stock symbol
        setCurrentStock(prev => ({
          ...prev,
          symbol: data.symbol
        }));
        console.log('Symbol set to:', data.symbol);
        
        // Fetch and display data
        await fetchData(data.symbol, data.period);
      }
    } catch (error) {
      console.error('Error fetching last chart:', error);
    }
  };
  

  const handleSymbolChange = (newSymbol: string) => {
    if (!newSymbol) return;
    fetchData(newSymbol, selectedPeriod);
  };

  const handlePeriodChange = (newPeriod: string) => {
    setSelectedPeriod(newPeriod);
    if (currentStock.symbol) {
      fetchData(currentStock.symbol, newPeriod);
    }
  };

  const handleStrategyChange = (strategy: string) => {
    setSelectedStrategy(strategy);
  };

  const handleRunScript = async (script: string) => {
    try {
      const response = await fetch('http://localhost:5001/run_script', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script }),
      });

      const result = await response.json();
      console.log('Script Result:', result);
      // Handle the result as needed
    } catch (error) {
      console.error('Error running script:', error);
    }
  };

  const handleAccountClick = () => {
    setIsLoginPageActive(true);
  };

  const handleLogin = (user: any) => {
    setLoggedInUser(user);
    setIsLoginPageActive(false);
  };

  const handleShowTechnicals = () => {
    setShowTechnicalsOverlay(true);
  };

  const handleCloseTechnicals = () => {
    setShowTechnicalsOverlay(false);
  };

  const handleLayoutChange = (layout: string) => {
    setSelectedLayout(layout);
    const symbolCount = {
      'single': 1,
      'horizontal-2': 2,
      'vertical-2': 2,
      'triple': 3,
      'quad': 4,
      'horizontal-3': 3,
      'vertical-3': 3
    }[layout] || 1;

    const newSymbols = [...symbols];
    while (newSymbols.length < symbolCount) {
      newSymbols.push('BTCUSDT');
    }
    setSymbols(newSymbols.slice(0, symbolCount));
  };

  return (
    <main className="flex flex-col h-screen bg-[#1E1E1E] text-white overflow-hidden">
      {!isLoginPageActive && (
        <TopPanel
          onSymbolChange={handleSymbolChange}
          selectedPeriod={selectedPeriod}
          onPeriodChange={handlePeriodChange}
          selectedStrategy={selectedStrategy}
          onStrategyChange={handleStrategyChange}
          currentStock={currentStock}
          selectedLayout={selectedLayout}
          onLayoutChange={handleLayoutChange}
        />
      )}
      
      <div className="flex flex-1 min-h-0">
        {/* Left section - NO RESIZER between chart and drawing tools */}
        <div className="flex h-full">
          <LeftSidePane onAccountClick={handleAccountClick} onChartClick={handleChartClick} />
          <DrawingTools />
        </div>
        {/* Middle section with more flexible limits */}
        <div className="flex flex-col flex-1 min-w-0">
          <Resizable
            defaultSize={{ width: '100%', height: '70%' }}
            minHeight={100}
            maxHeight="95%"
            enable={{ bottom: true }}
            handleClasses={{ bottom: 'h-1 bg-[#2a2a2a] hover:bg-blue-500 cursor-row-resize' }}
            style={{ overflow: 'hidden' }}
          >
            <MainChartContainer
              layout={selectedLayout}
              symbols={symbols}
              selectedPeriod={selectedPeriod}
              selectedStrategy={selectedStrategy}
            />
          </Resizable>
          
          {/* Give ScriptEditor proper height and container */}
          <div className="flex-1 min-h-[200px] overflow-hidden">
            <ScriptEditor onRunScript={handleRunScript} />
          </div>
        </div>
        {/* Right section with more flexible limits */}
        <Resizable
          defaultSize={{ width: '275px', height: '100%' }}
          minWidth={100} // Reduced from 200
          maxWidth={800} // Increased from 500
          enable={{ left: true }}
          handleClasses={{ left: 'w-1 bg-[#2a2a2a] hover:bg-blue-500 cursor-col-resize' }}
        >
          <Sidebar 
            currentStock={currentStock} 
            onShowTechnicals={handleShowTechnicals} 
          />
        </Resizable>
      </div>

      {loggedInUser && (
        <div className="absolute top-0 right-0 p-4 text-white">
          Logged in as: {loggedInUser.name}
        </div>
      )}

      {isLoginPageActive && (
        <div className="fixed inset-0 z-50 flex">
          <LeftSidePane 
            className="w-10 flex-shrink-0 bg-[#252526]" 
            onAccountClick={handleAccountClick} 
            onChartClick={handleChartClick}  // Add this line
          />
          <div className="flex-1 min-w-0 overflow-hidden -mr-[1px] bg-[#1E1E1E]">
            <LoginPage onLogin={handleLogin} />
          </div>
        </div>
      )}

{showTechnicalsOverlay && (
  <div className="fixed inset-0 z-50 flex">
    <LeftSidePane 
      className="w-10 flex-shrink-0 bg-[#252526]" 
      onAccountClick={handleAccountClick} 
      onChartClick={handleChartClick}  // Add this line
    />
    <div className="flex-1 bg-[#1E1E1E]">
      <div className="flex justify-end p-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={handleCloseTechnicals}
          className="text-[#666] hover:text-white hover:bg-[#2a2a2a]"
        >
          <X className="h-5 w-5" />
        </Button>
      </div>
      <div className="p-6">
        <Technicals 
          symbol={currentStock.symbol} 
          timeframe={selectedPeriod} 
          onClose={handleCloseTechnicals}
        />
      </div>
    </div>
    <div className="w-[275px] flex-shrink-0 border-l border-gray-700 bg-[#252526]">
      <Sidebar className="h-full" currentStock={currentStock} onShowTechnicals={handleShowTechnicals} />
    </div>
  </div>
)}

    </main>
  );
}
