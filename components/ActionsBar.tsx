import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PostIdeaModal } from './PostIdeaModal';
import html2canvas from 'html2canvas';
import { storage, db } from '../firebase/config';
import { ref, uploadString, getDownloadURL } from 'firebase/storage';
import { collection, addDoc } from 'firebase/firestore';
import { useAuth } from '../context/AuthContext';

const TRADING_CATEGORIES = ['Technical Analysis', 'Fundamental Analysis', 'Price Action', 'Pattern Trading', 'Swing Trading', 'Day Trading'];
const MARKETS = ['Crypto', 'Forex', 'Stocks', 'Commodities', 'Indices'];
const TRADING_TOOLS = {
  technical: ['RSI', 'MACD', 'Moving Averages', 'Bollinger Bands', 'Fibonacci'],
  fundamental: ['News Analysis', 'Economic Calendar', 'Financial Statements', 'Market Sentiment']
};

export default function ActionsBar() {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showPostModal, setShowPostModal] = useState(false);
  const [chartImage, setChartImage] = useState<string | null>(null);
  const { user } = useAuth();

  const captureChart = async () => {
    console.log('Capturing chart...');
    const chartElement = document.querySelector('.tradingview-chart');
    if (chartElement) {
      const canvas = await html2canvas(chartElement);
      console.log('Chart captured successfully');
      return canvas.toDataURL('image/png');
    }
    console.log('Chart element not found');
    return null;
  };

  const handlePostClick = async () => {
    console.log('Post button clicked');
    setShowPostModal(true);
    setIsExpanded(false);
    
    const capturedImage = await captureChart();
    if (capturedImage) {
      setChartImage(capturedImage);
    }
  };

  const handlePostIdea = async (data: { 
    title: string; 
    description: string;
    categories: string[];
    market: string;
    tools: string[];
  }) => {
    if (!user || !chartImage) return;

    try {
      const imageRef = ref(storage, `trading-ideas/${Date.now()}-chart.png`);
      await uploadString(imageRef, chartImage, 'data_url');
      const imageUrl = await getDownloadURL(imageRef);

      await addDoc(collection(db, 'trading-ideas'), {
        title: data.title,
        description: data.description,
        chartImage: imageUrl,
        categories: data.categories,
        market: data.market,
        tools: data.tools,
        author: {
          id: user.uid,
          name: user.displayName,
          avatar: user.photoURL
        },
        createdAt: new Date(),
        likes: 0,
        comments: []
      });

      setShowPostModal(false);
      setChartImage(null);
    } catch (error) {
      console.error('Error posting idea:', error);
    }
  };

  return (
    <>
      <motion.div 
        drag
        dragMomentum={false}
        className="fixed bottom-6 right-6 z-50"
      >
        <motion.div 
          className="bg-[#242424] rounded-lg shadow-lg"
          animate={{ width: isExpanded ? 'auto' : '48px' }}
        >
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-12 h-12 flex items-center justify-center text-white hover:bg-[#2a2a2a] rounded-lg"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </button>

          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="p-4 space-y-4"
              >
                <button
                  onClick={handlePostClick}
                  className="w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors"
                >
                  Post Idea
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </motion.div>

      {showPostModal && (
        <PostIdeaModal
          onClose={() => {
            setShowPostModal(false);
            setChartImage(null);
          }}
          onPost={handlePostIdea}
          previewImage={chartImage}
          categories={TRADING_CATEGORIES}
          markets={MARKETS}
          tools={TRADING_TOOLS}
        />
      )}
    </>
  );
}
