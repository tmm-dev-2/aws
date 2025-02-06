export function MarketOverview({ data }) {
  if (!data) return null

  return (
    <div className="bg-[#252526] rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Market Movers</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-green-500 mb-2">Top Gainers</h3>
          {data.gainers.map((stock) => (
            <div key={stock.symbol} className="flex justify-between py-2">
              <span>{stock.symbol}</span>
              <span className="text-green-500">+{stock.change.toFixed(2)}%</span>
            </div>
          ))}
        </div>
        <div>
          <h3 className="text-red-500 mb-2">Top Losers</h3>
          {data.losers.map((stock) => (
            <div key={stock.symbol} className="flex justify-between py-2">
              <span>{stock.symbol}</span>
              <span className="text-red-500">{stock.change.toFixed(2)}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
