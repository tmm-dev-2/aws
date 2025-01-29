import React, { useState, useEffect } from 'react';
import { TopPanel } from './top-panel';
import { MainChartContainer } from './main-chart';
import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';

export const TradingView: React.FC = () => {
  const [selectedLayout, setSelectedLayout] = useState('single');
  const [symbols, setSymbols] = useState(['BTCUSDT']);
  const [selectedPeriod, setSelectedPeriod] = useState('1d');
  const [selectedStrategy, setSelectedStrategy] = useState('none');
  const [loggedInUser, setLoggedInUser] = useState<User | null>(null);

  useEffect(() => {
    // Load last viewed symbols from Firebase
    const loadLastViewed = async () => {
      const db = getFirestore();
      const lastChartRef = doc(db, 'userCharts', loggedInUser?.googleId || 'default');
      const docSnap = await getDoc(lastChartRef);
      
      if (docSnap.exists()) {
        const data = docSnap.data();
        setSymbols(data.symbols || ['BTCUSDT']);
        setSelectedLayout(data.layout || 'single');
      }
    };

    if (loggedInUser) {
      loadLastViewed();
    }
  }, [loggedInUser]);

  // Save layout and symbols when they change
  useEffect(() => {
    const saveLayout = async () => {
      const db = getFirestore();
      const lastChartRef = doc(db, 'userCharts', loggedInUser?.googleId || 'default');
      await setDoc(lastChartRef, {
        symbols,
        layout: selectedLayout,
        timestamp: new Date()
      }, { merge: true });
    };

    if (loggedInUser) {
      saveLayout();
    }
  }, [symbols, selectedLayout, loggedInUser]);

  const handleLayoutChange = (layout: string) => {
    setSelectedLayout(layout);
    // Map layouts to required number of symbols
    const symbolCount = {
      'single': 1,
      'horizontal-2': 2,
      'vertical-2': 2,
      'triple': 3,
      'quad': 4,
      'horizontal-3': 3,
      'vertical-3': 3
    }[layout] || 1;

    // Update symbols array based on new layout
    const newSymbols = [...symbols];
    while (newSymbols.length < symbolCount) {
      newSymbols.push('BTCUSDT'); // Default symbol for new charts
    }
    setSymbols(newSymbols.slice(0, symbolCount));
  };

  const handleSymbolChange = (index: number, newSymbol: string) => {
    const updatedSymbols = [...symbols];
    updatedSymbols[index] = newSymbol;
    setSymbols(updatedSymbols);
  };

  return (
    <div className="h-screen flex flex-col bg-[#131722]">
      <TopPanel
        onSymbolChange={(symbol) => handleSymbolChange(0, symbol)}
        onPeriodChange={setSelectedPeriod}
        onStrategyChange={setSelectedStrategy}
        onLayoutChange={handleLayoutChange}
        selectedPeriod={selectedPeriod}
        selectedStrategy={selectedStrategy}
        selectedLayout={selectedLayout}
      />
      <div className="flex-1">
        <MainChartContainer
          layout={selectedLayout}
          symbols={symbols}
          selectedPeriod={selectedPeriod}
          selectedStrategy={selectedStrategy}
        />
      </div>
    </div>
  );
};
