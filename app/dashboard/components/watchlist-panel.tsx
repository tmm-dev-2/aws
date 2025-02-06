import { useState, useEffect } from 'react'

export function WatchlistPanel() {
  const [watchlist, setWatchlist] = useState([])
  const defaultSymbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

  useEffect(() => {
    fetchWatchlistData()
    const interval = setInterval(fetchWatchlistData, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchWatchlistData = async () => {
    const response = await fetch(`http://localhost:5000/fetch_multiple_stocks?symbols=${defaultSymbols.join(',')}`)
    const data = await response.json()
    setWatchlist(data)
  }

  return (
    <div className="bg-[#252526] rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Watchlist</h2>
      <div className="grid grid-cols-6 gap-4">
        {watchlist.map((stock) => (
          <div key={stock.symbol} className="p-4 bg-[#1E1E1E] rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium">{stock.symbol}</span>
              <span className={stock.change > 0 ? 'text-green-500' : 'text-red-500'}>
                {Number(stock.changePercent).toFixed(2)}%
              </span>
            </div>
            <div className="mt-2">
              <span className="text-2xl">${Number(stock.price).toFixed(2)}</span>
            </div>
            <div className="text-sm text-gray-400 mt-2">
              {stock.companyName}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
