const trends = [
  {
    name: "ICICIBANK",
    fullName: "ICICI BANK LTD.",
    price: "1,254.50",
    change: "-0.08%",
    isNegative: true,
  },
  {
    name: "INFY",
    fullName: "INFOSYS LTD",
    price: "1,863.00",
    change: "+0.63%",
    isNegative: false,
  },
  {
    name: "ADANIENT",
    fullName: "ADANI ENTERPRISES LTD",
    price: "2,270.00",
    change: "-0.78%",
    isNegative: true,
  },
]

const volumeStocks = [
  {
    name: "KALYAN JEWELLERS IND LTD",
    symbol: "KALYANKJIL",
    price: "502.50",
    change: "-0.58%",
  },
  {
    name: "ZOMATO LTD",
    symbol: "ZOMATO",
    price: "235.02",
    change: "-0.55%",
  },
]

export function CommunityTrends() {
  return (
    <div className="mt-4 grid gap-8 lg:grid-cols-2">
      <div className="space-y-4">
        <h3 className="font-medium">Trending stocks</h3>
        <div className="grid gap-4">
          {trends.map((trend) => (
            <div key={trend.name} className="flex items-center justify-between rounded-lg border p-4">
              <div>
                <p className="font-medium">{trend.name}</p>
                <p className="text-sm text-muted-foreground">{trend.fullName}</p>
              </div>
              <div className="text-right">
                <p className="font-medium">{trend.price}</p>
                <p className={trend.isNegative ? "text-sm text-red-500" : "text-sm text-green-500"}>{trend.change}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="space-y-4">
        <h3 className="font-medium">Highest volume stocks</h3>
        <div className="grid gap-4">
          {volumeStocks.map((stock) => (
            <div key={stock.name} className="flex items-center justify-between rounded-lg border p-4">
              <div>
                <p className="font-medium">{stock.name}</p>
                <p className="text-sm text-muted-foreground">{stock.symbol}</p>
              </div>
              <div className="text-right">
                <p className="font-medium">{stock.price}</p>
                <p className="text-sm text-red-500">{stock.change}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

