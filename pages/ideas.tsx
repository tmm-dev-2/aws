import React, { useState, useEffect } from 'react';
import { storage, db } from '../firebase/config';
import { collection, addDoc, query, orderBy, onSnapshot } from 'firebase/firestore';
import { ref, uploadString, getDownloadURL } from 'firebase/storage';
import { useAuth } from '../context/AuthContext';
import { PostIdeaModal } from '../components/PostIdeaModal';
import { MultiSelect } from '../components/MultiSelect';
import html2canvas from 'html2canvas';
import '../app/globals.css';

const TRADING_CATEGORIES = ['Technical Analysis', 'Fundamental Analysis', 'Price Action', 'Pattern Trading', 'Swing Trading', 'Day Trading'];
const MARKETS = ['Crypto', 'Forex', 'Stocks', 'Commodities', 'Indices'];
const TRADING_TOOLS = {
  technical: ['RSI', 'MACD', 'Moving Averages', 'Bollinger Bands', 'Fibonacci'],
  fundamental: ['News Analysis', 'Economic Calendar', 'Financial Statements', 'Market Sentiment']
};

interface TradingIdea {
    id: string;
    title: string;
    description: string;
    chartImage: string;
    categories: string[];
    market: string;
    tools: string[];
    author: {
        id: string;
        name: string;
        avatar: string;
    };
    createdAt: {
        toDate: () => Date;
    };
    likes: number;
    reactions: {
        [key: string]: number;
    };
    comments: any[];
}

function IdeaCard({ idea }: { idea: TradingIdea }) {
  return (
    <div className="bg-[#242424] rounded-lg overflow-hidden shadow-lg">
      <img src={idea.chartImage} alt="Chart" className="w-full h-48 object-cover"/>
      <div className="p-4">
        <div className="flex items-center gap-2 mb-3">
          <img 
            src={idea.author.avatar || '/default-avatar.png'} 
            alt={idea.author.name} 
            className="w-8 h-8 rounded-full"
          />
          <span className="text-white">{idea.author.name}</span>
        </div>
        <h3 className="text-xl font-bold text-white mb-2">{idea.title}</h3>
        <p className="text-gray-300">{idea.description}</p>
        <div className="mt-4 flex flex-wrap gap-2">
          {idea.categories?.map((category, index) => (
            <span key={index} className="bg-blue-500/20 text-blue-400 text-sm px-2 py-1 rounded">
              {category}
            </span>
          ))}
        </div>
        <div className="mt-2">
          <span className="text-gray-400 text-sm">
            {idea.createdAt.toDate().toLocaleDateString()}
          </span>
        </div>
      </div>
    </div>
  );
}

export default function IdeasPage() {
    const [ideas, setIdeas] = useState<TradingIdea[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filters, setFilters] = useState({
        categories: [] as string[],
        market: '',
        tools: [] as string[]
    });
    const [isPostingIdea, setIsPostingIdea] = useState(false);
    const { user } = useAuth();
    const [chartImage, setChartImage] = useState<string | null>(null);

    useEffect(() => {
        const ideasRef = collection(db, 'ideas');
        const q = query(ideasRef, orderBy('createdAt', 'desc'));
        
        const unsubscribe = onSnapshot(q, (snapshot) => {
            const ideasData = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            })) as TradingIdea[];
            console.log('Fetched ideas:', ideasData);
            setIdeas(ideasData);
        });

        return () => unsubscribe();
    }, []);

    const captureChart = async () => {
        const chartElement = document.querySelector('#tradingview_chart') as HTMLElement;
        if (chartElement) {
            const canvas = await html2canvas(chartElement);
            return canvas.toDataURL('image/png');
        }
        return null;
    };

    const handlePostClick = async () => {
        const capturedChartImage = await captureChart();
        if (capturedChartImage) {
            setChartImage(capturedChartImage);
            setIsPostingIdea(true);
        }
    };

    const filteredIdeas = ideas.filter(idea => {
        const matchesSearch = idea.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            idea.description.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesCategory = filters.categories.length === 0 || 
                              idea.categories?.some(cat => filters.categories.includes(cat));
        const matchesMarket = !filters.market || idea.market === filters.market;
        
        return matchesSearch && matchesCategory && matchesMarket;
    });

    return (
        <div className="min-h-screen bg-[#1a1a1a] p-6">
            <div className="max-w-6xl mx-auto">
                <div className="mb-6 space-y-4">
                    <input
                        type="text"
                        placeholder="Search ideas..."
                        className="w-full bg-[#242424] text-white p-3 rounded"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    
                    <div className="flex gap-4">
                        <MultiSelect
                            options={TRADING_CATEGORIES}
                            value={filters.categories}
                            onChange={(val) => setFilters(prev => ({...prev, categories: val}))}
                            placeholder="Filter by Categories"
                        />
                        
                        <select
                            value={filters.market}
                            onChange={(e) => setFilters(prev => ({...prev, market: e.target.value}))}
                            className="bg-[#242424] text-white p-2 rounded"
                        >
                            <option value="">All Markets</option>
                            {MARKETS.map(market => (
                                <option key={market} value={market}>{market}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {filteredIdeas.map(idea => (
                        <IdeaCard key={idea.id} idea={idea} />
                    ))}
                </div>
            </div>
            
            <button 
                onClick={handlePostClick}
                className="fixed bottom-6 right-6 bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full shadow-lg z-10 flex items-center gap-2"
            >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Post Idea
            </button>
            
            {isPostingIdea && (
                <PostIdeaModal 
                    onClose={() => setIsPostingIdea(false)}
                    onPost={async (data) => {
                        if (!user || !chartImage) return;

                        const imageRef = ref(storage, `charts/${Date.now()}-chart.png`);
                        await uploadString(imageRef, chartImage, 'data_url');
                        const imageUrl = await getDownloadURL(imageRef);

                        await addDoc(collection(db, 'ideas'), {
                            ...data,
                            chartImage: imageUrl,
                            author: {
                                id: user.uid,
                                name: user.displayName,
                                avatar: user.photoURL
                            },
                            createdAt: new Date(),
                            likes: 0,
                            comments: []
                        });

                        setIsPostingIdea(false);
                    }}
                    categories={TRADING_CATEGORIES}
                    markets={MARKETS}
                    tools={TRADING_TOOLS}
                />
            )}
        </div>
    );
}
