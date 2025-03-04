const news = [
  {
    title: "Buy these 9 budget-sensitive stocks as FM aims to boost consumption while maintaining fiscal path",
    source: "Moneycontrol",
    timeAgo: "14 hours ago",
  },
  {
    title: "Seven key sectors that will be in spotlight post Budget 2025",
    source: "Moneycontrol",
    timeAgo: "15 hours ago",
  },
  {
    title: "FIIs net sell shares worth Rs 1,327 crore, DIIs net buy shares worth Rs 824 crore",
    source: "Moneycontrol",
    timeAgo: "16 hours ago",
  },
  {
    title: "Stocks across auto, FMCG, healthcare stand to gain from Union Budget 2025",
    source: "Moneycontrol",
    timeAgo: "17 hours ago",
  },
  {
    title: "Budget is done! Bulls need to keep Nifty above 23,280 for further momentum, say technical analysts",
    source: "Moneycontrol",
    timeAgo: "18 hours ago",
  },
]

export function StockNews() {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold">Indian stocks news</h2>
      <div className="grid gap-4">
        {news.map((item) => (
          <div key={item.title} className="rounded-lg border p-4 transition-colors hover:bg-muted/50">
            <div className="space-y-1">
              <h3 className="font-medium leading-none">{item.title}</h3>
              <div className="flex items-center text-sm text-muted-foreground">
                <span>{item.source}</span>
                <span className="mx-2">•</span>
                <span>{item.timeAgo}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div>
        <a href="#" className="text-sm text-blue-500 hover:underline">
          Keep reading
        </a>
      </div>
    </div>
  )
}

