'use client'

import '../app/globals.css';
import React from 'react';
import { Sidebar } from '../components/sidebar';
import { ChevronDown, Plus, MoreHorizontal, Copy, Pencil, Layout, Trash, FilePlus, Download, FolderOpen, LucideToggleLeft, Bell } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { Button } from 'dashboard/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from 'dashboard/components/ui/card';
import { Input } from 'dashboard/components/ui/input';

interface StockSuggestion {
  symbol: string;
  name: string;
}

interface WatchlistItem {
  symbol: string;
  last: string;
  chg: string;
  chgPercent: string;
}

const mockStock = {
  symbol: 'AAPL',
  price: 150.23,
  change: 2.5,
  changePercent: 1.67,
  companyName: 'Apple Inc.',
  exchange: 'NASDAQ',
  industry: 'Technology',
  lastUpdated: '2024-01-19 16:00:00',
  previousClose: 148.50,
  open: 151.00,
  dayLow: 149.75,
  dayHigh: 152.50,
  volume: 1000000,
  marketCap: 2.5e12,
  peRatio: 30.5,
  eps: 4.90,
  dividendYield: 0.005,
  beta: 1.2,
  fiftyTwoWeekHigh: 175.00,
  fiftyTwoWeekLow: 130.00,
  employees: 150000,
  headquarters: 'Cupertino, CA',
  description:
    'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories.',
  ceo: 'Tim Cook',
};

export default function WatchlistPage() {
  const [isPopupVisible, setIsPopupVisible] = React.useState(false);
  const [isCreateListPopupVisible, setIsCreateListPopupVisible] = React.useState(false);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [newWatchlistName, setNewWatchlistName] = React.useState('');
  const [suggestions, setSuggestions] = React.useState<StockSuggestion[]>([]);
  const [watchlist, setWatchlist] = React.useState<WatchlistItem[]>([]);
  const [watchlists, setWatchlists] = React.useState<{ name: string }[]>([]);

  React.useEffect(() => {
    const fetchWatchlists = async () => {
      try {
        const response = await fetch('/watchlists');
        if (response.ok) {
          const data = await response.json();
          setWatchlists(data);
        } else {
          console.error('Failed to fetch watchlists');
        }
      } catch (error) {
        console.error('Error fetching watchlists:', error);
      }
    };

    fetchWatchlists();
  }, []);

  const togglePopup = () => {
    setIsPopupVisible(!isPopupVisible);
  };

  const fetchSuggestions = async (query: string) => {
    if (query) {
      try {
        const response = await fetch(`/api/get_stock_suggestions?query=${query}`);
        if (response.ok) {
          const data: StockSuggestion[] = await response.json();
          setSuggestions(data);
        } else {
          console.error('Failed to fetch suggestions');
        }
      } catch (error) {
        console.error('Error fetching suggestions:', error);
      }
    } else {
      setSuggestions([]);
    }
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const query = event.target.value;
    setSearchQuery(query);
    fetchSuggestions(query);
  };

  const addToWatchlist = async (symbol: string) => {
    try {
      const response = await fetch('/api/watchlist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbols: [symbol] }),
      });

      if (response.ok) {
        const data: WatchlistItem[] = await response.json();
        setWatchlist((prevWatchlist) => [...prevWatchlist, ...data]);
        setIsPopupVisible(false);
      } else {
        console.error('Failed to add to watchlist');
      }
    } catch (error) {
      console.error('Error adding to watchlist:', error);
    }
  };

  const handleCreateList = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await fetch('/api/watchlist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newWatchlistName }),
      });

      if (response.ok) {
        console.log('Watchlist created successfully');
        setIsCreateListPopupVisible(false);
        // Optionally refresh the watchlist list here
      } else {
        console.error('Failed to create watchlist');
      }
    } catch (error) {
      console.error('Error creating watchlist:', error);
    }
  };

  return (
    <main className="flex h-screen text-white bg-[#1a1a1a]">
      <div className="flex-1 flex flex-col">
        {/* Top panel */}
        <div className="flex items-center justify-between p-4 border-b border-[#333333]">
          <div className="flex items-center gap-2 relative">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="flex items-center gap-2 text-lg font-semibold bg-transparent hover:bg-[#333333] text-white p-2 rounded-md">
                  Watchlist
                  <ChevronDown className="h-4 w-4" />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56 bg-[#1a1a1a] border-[#333333] text-white">
                {watchlists.map((list) => (
                  <DropdownMenuItem key={list.name} className="hover:bg-[#333333] focus:bg-[#333333]">
                    {list.name}
                  </DropdownMenuItem>
                ))}
                <div className="flex items-center justify-between px-3 py-2">
                  <LucideToggleLeft className="h-4 w-4" />
                  <span>Share list</span>
                  <Switch />
                </div>
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]">
                  <Bell className="h-4 w-4" />
                  Create alert on list...
                  <span className="ml-2 text-xs bg-yellow-500 text-black px-1 rounded">NEW</span>
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]">
                  <Copy className="h-4 w-4" />
                  Make a copy...
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]">
                  <Pencil className="h-4 w-4" />
                  Rename
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]">
                  <Layout className="h-4 w-4" />
                  Add section
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]">
                  <Trash className="h-4 w-4" />
                  Clear list
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-[#333333]" />
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]"onClick={() => setIsCreateListPopupVisible(true)}>
                  <FilePlus className="h-4 w-4" />
                  Create new list...
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]" >
                  <Download className="h-4 w-4" />
                  Import list...
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-[#333333] focus:bg-[#333333]">
                  <FolderOpen className="h-4 w-4" />
                  Open list...
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 hover:bg-[#333333] rounded-md" onClick={togglePopup}>
              <Plus className="h-4 w-4" />
            </button>
            <button className="p-2 hover:bg-[#333333] rounded-md">
              <MoreHorizontal className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Table header */}
        <div className="grid grid-cols-4 px-4 py-2 text-sm text-gray-400 border-b border-[#333333]">
          <div>Symbol</div>
          <div className="text-right">Last</div>
          <div className="text-right">Chg</div>
          <div className="text-right">Chg%</div>
        </div>

        {/* Table content */}
        <div className="flex-1 overflow-auto">
          {watchlist.map((item) => (
            <div key={item.symbol} className="grid grid-cols-4 px-4 py-2 text-sm hover:bg-[#242424] cursor-pointer">
              <div>{item.symbol}</div>
              <div className="text-right">{item.last}</div>
              <div className="text-right" style={{ color: parseFloat(item.chg) < 0 ? '#ff4d4d' : '#00ff88' }}>
                {item.chg}
              </div>
              <div className="text-right" style={{ color: parseFloat(item.chgPercent) < 0 ? '#ff4d4d' : '#00ff88' }}>
                {item.chgPercent}%
              </div>
            </div>
          ))}
        </div>
        {isPopupVisible && (
          <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#1a1a1a] p-6 rounded-md shadow-lg border border-[#333333]">
            <Card>
              <CardHeader>
                <CardTitle>Add Symbol to Watchlist</CardTitle>
                <CardDescription>Enter the symbol to add to the watchlist.</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <Input
                    type="text"
                    placeholder="Search stocks..."
                    value={searchQuery}
                    onChange={handleSearchChange}
                    className="bg-[#242424] border border-[#333333] rounded-md px-2 py-1 text-sm focus:outline-none w-64"
                  />
                  <button className="p-2 hover:bg-[#333333] rounded-md" onClick={() => {
                    if (searchQuery.trim() !== '') {
                      addToWatchlist(searchQuery);
                    }
                  }}>
                    <Plus className="h-4 w-4" />
                  </button>
                </div>
                {suggestions.length > 0 && (
                  <ul className="mt-2 w-64 bg-[#1a1a1a] border border-[#333333] rounded-md shadow-md z-10">
                    {suggestions.map((suggestion) => (
                      <li
                        key={suggestion.symbol}
                        className="px-4 py-2 text-sm hover:bg-[#333333] cursor-pointer"
                        onClick={() => addToWatchlist(suggestion.symbol)}
                      >
                        {suggestion.name} ({suggestion.symbol})
                      </li>
                    ))}
                  </ul>
                )}
                <button onClick={togglePopup} className="mt-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
                  Close
                </button>
              </CardContent>
            </Card>
          </div>
        )}
        {isCreateListPopupVisible && (
          <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#1a1a1a] p-6 rounded-md shadow-lg border border-[#333333]">
            <Card>
              <CardHeader>
                <CardTitle>Create New Watchlist</CardTitle>
                <CardDescription>Enter the name for the new watchlist.</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCreateList} className="flex flex-col gap-4">
                  <Input
                    type="text"
                    placeholder="Watchlist name"
                    className="bg-[#242424] border border-[#333333] rounded-md px-2 py-1 text-sm focus:outline-none w-full"
                    onChange={(e) => setNewWatchlistName(e.target.value)}
                  />
                  <div className="flex justify-end gap-2">
                    <Button type="submit" className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                      Create
                    </Button>
                    <button type="button" onClick={() => setIsCreateListPopupVisible(false)} className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
                      Close
                    </button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
      <div className="w-[350px] bg-[#1a1a1a] border-l border-[#333333]">
        <Sidebar currentStock={mockStock} />
      </div>
    </main>
  );
}
