const stories = [
  {
    title: "PCE Inflation Accelerated in December",
    source: "Dow Jones Newswires",
    timeAgo: "2 days ago",
  },
  {
    title: "EUR/USD: Euro Slides Under $1.04 as Flurry of News Triggers Forex Markets",
    source: "TradingView",
    timeAgo: "2 days ago",
    isHot: true,
  },
  {
    title: "XAU/USD: Gold Breaks Out to New Record at $2,800 as Trump Follows Through on Tarifs",
    source: "TradingView",
    timeAgo: "2 days ago",
    isHot: true,
  },
]

export function TopStories() {
  return (
    <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {stories.map((story) => (
        <div key={story.title} className="flex items-start space-x-4 rounded-lg border p-4">
          <div className="flex-1 space-y-1">
            <p className="text-sm font-medium leading-none">{story.title}</p>
            <div className="flex items-center space-x-2">
              <p className="text-sm text-muted-foreground">{story.source}</p>
              <span className="text-sm text-muted-foreground">•</span>
              <p className="text-sm text-muted-foreground">{story.timeAgo}</p>
              {story.isHot && <span className="text-sm text-red-500">🔥 Hot</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

