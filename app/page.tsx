"use client"

import { useState, useEffect } from 'react';
import { Button } from "components/ui/button";
import { MainChart, MainChartContainer } from "components/main-chart";
import { Sidebar } from "components/sidebar";
import { DrawingTools } from "components/drawing-tools";
import { TopPanel } from "components/top-panel";
import { LeftSidePane } from "components/left-side-pane";
import dynamic from 'next/dynamic'
import LoginPage from 'components/auth/LoginPage';
import { X } from 'lucide-react';
import Technicals from "../components/Technicals";
import { Resizable } from 're-resizable';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';
import { TradingView } from '../components/tmm-chart'
import ActionsBar from "components/ActionsBar";
import ProfilePage from '../components/ProfilePage';
import { auth } from '../config/firebase';
import { AIResults } from '../components/ai-results/ai-results';
import { Workspace } from "components/space";


const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET!,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID!,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID!
};

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
    symbol: 'BTCUSDT',
    price: 0,
    change: 0,
    changePercent: 0,
    lastUpdated: '',
    companyName: 'Bitcoin',
    exchange: 'BINANCE',
    industry: 'Cryptocurrency'
  });
  const [isLoginPageActive, setIsLoginPageActive] = useState(false);
  const [loggedInUser, setLoggedInUser] = useState<User | null>(null);
  const [showTechnicalsOverlay, setShowTechnicalsOverlay] = useState(false);
  const [lastChartData, setLastChartData] = useState<{symbol: string, period: string} | null>(null);
  const [selectedLayout, setSelectedLayout] = useState('single');
  const [symbols, setSymbols] = useState(['BTCUSDT']);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [showAIResults, setShowAIResults] = useState(false);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        setIsAuthenticated(true);
        setLoggedInUser(user);
      }
    });
  
    return () => unsubscribe();
  }, []);

  const fetchData = async (symbol: string, period: string) => {
    if (!symbol || symbol === 'undefined') return;
    
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
        throw new Error(`Failed to fetch data: ${response.statusText}`);
      }

      const rawData = await response.json();
      
      if (!rawData || !Array.isArray(rawData) || rawData.length === 0) {
        throw new Error('No data received from server');
      }

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

        if (loggedInUser?.googleId) {
          const lastChartRef = doc(db, 'userCharts', loggedInUser.googleId);
          await setDoc(lastChartRef, {
            symbol,
            period,
            timestamp: new Date()
          });
        }
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setCurrentStock(prev => ({
        ...prev,
        symbol: 'BTCUSDT',
        exchange: 'BINANCE'
      }));
    }
  };

  const handleChartClick = async () => {
    setIsLoginPageActive(false);
    setShowTechnicalsOverlay(false);
    setShowAIResults(false);
  
    try {
      if (loggedInUser?.googleId) {
        const lastChartRef = doc(db, 'userCharts', loggedInUser.googleId);
        const docSnap = await getDoc(lastChartRef);
        
        if (docSnap.exists()) {
          const data = docSnap.data();
          setSelectedPeriod(data.period);
          setCurrentStock(prev => ({
            ...prev,
            symbol: data.symbol
          }));
          await fetchData(data.symbol, data.period);
        }
      }
    } catch (error) {
      console.error('Error fetching last chart:', error);
    }
  };

  const handleSymbolChange = (newSymbol: string) => {
    if (!newSymbol || newSymbol === 'undefined') {
      console.error('Invalid symbol received');
      return;
    }
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
    } catch (error) {
      console.error('Error running script:', error);
    }
  };

  const handleAccountClick = () => {
    setIsLoginPageActive(true);
    setShowAIResults(false);
  };

  const handleLogin = (user: any) => {
    setLoggedInUser(user);
    setIsLoginPageActive(false);
  };

  const handleShowTechnicals = () => {
    setShowTechnicalsOverlay(true);
    setShowAIResults(false);
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

  const handleAnalysisResults = () => {
    setShowAIResults(true);
  };

  return (
    <main className="flex flex-col h-screen bg-[#1E1E1E] text-white overflow-hidden">
      {!isLoginPageActive && !showAIResults && (
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
        <div className="flex h-full">
          <LeftSidePane onAccountClick={handleAccountClick} onChartClick={handleChartClick} />
          <DrawingTools />
        </div>
        
        {showAIResults ? (
          <div className="flex-1 relative">
            <Button
              className="absolute top-4 right-4 z-50"
              variant="ghost"
              size="icon"
              onClick={() => setShowAIResults(false)}
            >
              <X className="h-5 w-5" />
            </Button>
            <AIResults />
          </div>
        ) : (
          <div className="flex flex-col flex-1 min-w-0">
            <Resizable
              defaultSize={{ width: '100%', height: '70%' }}
              minHeight={300}
              maxHeight="80%"
              enable={{ bottom: true }}
              handleClasses={{ bottom: 'h-1 bg-[#2a2e39] hover:bg-blue-500 cursor-row-resize' }}
              style={{ overflow: 'hidden' }}
            >
              <MainChartContainer
                layout={selectedLayout}
                symbols={symbols}
                selectedPeriod={selectedPeriod}
                selectedStrategy={selectedStrategy}
                onAnalysisResults={handleAnalysisResults}
              />
            </Resizable>
            
            <div className="flex-1 min-h-[200px] overflow-hidden">
            <Workspace />
            </div>
          </div>
        )}

        <Resizable
          defaultSize={{ width: '275px', height: '100%' }}
          minWidth={100}
          maxWidth={800}
          enable={{ left: true }}
          handleClasses={{ left: 'w-1 bg-[#2a2e39] hover:bg-blue-500 cursor-col-resize' }}
        >
          <Sidebar 
            currentStock={currentStock} 
            onShowTechnicals={handleShowTechnicals}
            analysisResults={analysisResults} 
          />
        </Resizable>
      </div>

      {loggedInUser && (
        <div className="absolute top-0 right-0 p-4 text-white">
          Logged in as: {loggedInUser.name}
        </div>
      )}

      {isLoginPageActive && !isAuthenticated ? (
        <div className="fixed inset-0 z-50 flex">
          <LeftSidePane 
            className="w-10 flex-shrink-0 bg-[#252526]" 
            onAccountClick={handleAccountClick} 
            onChartClick={handleChartClick}
          />
          <div className="flex-1 min-w-0 overflow-hidden -mr-[1px] bg-[#1E1E1E]">
            <LoginPage onLogin={handleLogin} />
          </div>
        </div>
      ) : isLoginPageActive && isAuthenticated ? (
        <div className="fixed inset-0 z-50 flex">
          <LeftSidePane 
            className="w-10 flex-shrink-0 bg-[#252526]" 
            onAccountClick={handleAccountClick} 
            onChartClick={handleChartClick}
          />
          <div className="flex-1 min-w-0 overflow-hidden -mr-[1px] bg-[#1E1E1E]">
            <ProfilePage />
          </div>
        </div>
      ) : null}

      {showTechnicalsOverlay && (
        <div className="fixed inset-0 z-50 flex">
          <LeftSidePane 
            className="w-10 flex-shrink-0 bg-[#252526]" 
            onAccountClick={handleAccountClick} 
            onChartClick={handleChartClick}
          />
          <div className="flex-1 bg-[#1E1E1E]">
            <div className="flex justify-end p-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={handleCloseTechnicals}
                className="text-[#666] hover:text-white hover:bg-[#2a2e39]"
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
         </div>
       )}
 
       <ActionsBar />
     </main>
   );
 }
                
