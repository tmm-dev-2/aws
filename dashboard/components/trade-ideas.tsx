const trades = [
  {
    title: "KSB Ltd: Channel Breakout on Budget 2025 Irrigation Boost",
    description: "Details: Asset: KSB Ltd Breakout Level: Channel breakout confirmed",
    author: "CyborgTradingHub",
    timeAgo: "Feb 1",
    comments: 1,
    likes: 17,
  },
  {
    title: "BEL is bearish on monthly chart with RSI divergence,A big fall",
    description:
      "BEL is bearish on monthly chart with RSI Divergence ,in coming days it may fall badly with activation of XABCD pattern",
    author: "sushildutt2",
    timeAgo: "17 hours ago",
    comments: 1,
    likes: 3,
  },
  {
    title: "Education purpose only",
    description:
      "If stock holds the Daily EMA 20 after the bad news than it should bounce back to WEMA 20 DEMA 20 is 624 Very extreme hypothesis lets see how it play...",
    author: "navingoyal2003",
    timeAgo: "23 hours ago",
    comments: 3,
    likes: 0,
  },
]

export function TradeIdeas() {
  return (
    <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {trades.map((trade) => (
        <div key={trade.title} className="flex flex-col space-y-4 rounded-lg border p-4">
          <div className="aspect-[4/3] bg-muted/20">
            {/* Placeholder for chart */}
            <div className="flex h-full items-center justify-center">
              <p className="text-muted-foreground">Chart placeholder</p>
            </div>
          </div>
          <div className="space-y-2">
            <h3 className="font-medium">{trade.title}</h3>
            <p className="text-sm text-muted-foreground">{trade.description}</p>
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-2">
                <span>{trade.author}</span>
                <span>•</span>
                <span>{trade.timeAgo}</span>
              </div>
              <div className="flex items-center space-x-4">
                <span>{trade.comments} 💬</span>
                <span>{trade.likes} 👍</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

