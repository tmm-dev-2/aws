"use client"

import { Avatar } from "dashboard/components/ui/avatar"
import { Card } from "dashboard/components/ui/card"

const gainers = [
  {
    name: "ARCHIES LTD",
    symbol: "ARCHIES",
    price: "22.20",
    change: "-0.54",
    currency: "INR",
  },
  {
    name: "HINDUSTAN MOTORS LTD",
    symbol: "HINDMOTORS",
    price: "27.90",
    change: "+2.12",
    currency: "INR",
  },
  {
    name: "GP PETROLEUMS LTD",
    symbol: "GULFPETRO",
    price: "55.10",
    change: "+0.95",
    currency: "INR",
  },
]

const losers = [
  {
    name: "ONELIFE CAP ADVISORS LTD",
    symbol: "ONELIFECAP",
    price: "15.68",
    change: "-1.88",
    currency: "INR",
  },
  {
    name: "MCNALLY BH. ENG. CO.LTD",
    symbol: "MBECL",
    price: "3.60",
    change: "-0.55",
    currency: "INR",
  },
  {
    name: "REVATHI EQUIPMENT INDIA L",
    symbol: "RVTHI",
    price: "1,835.10",
    change: "-2.54",
    currency: "INR",
  },
]

export function StockMovers() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div>
        <h2 className="mb-4 text-lg font-semibold">Stock gainers</h2>
        <div className="space-y-4">
          {gainers.map((stock) => (
            <Card key={stock.symbol} className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <Avatar className="h-8 w-8">
                    <div className="flex h-full w-full items-center justify-center rounded-full bg-primary/10">
                      {stock.symbol[0]}
                    </div>
                  </Avatar>
                  <div>
                    <p className="font-medium">{stock.name}</p>
                    <p className="text-sm text-muted-foreground">{stock.symbol}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-medium">
                    {stock.price} {stock.currency}
                  </p>
                  <p className={Number(stock.change) > 0 ? "text-sm text-green-500" : "text-sm text-red-500"}>
                    {stock.change}%
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
        <div className="mt-4">
          <a href="#" className="text-sm text-blue-500 hover:underline">
            See all stocks with largest daily growth
          </a>
        </div>
      </div>
      <div>
        <h2 className="mb-4 text-lg font-semibold">Stock losers</h2>
        <div className="space-y-4">
          {losers.map((stock) => (
            <Card key={stock.symbol} className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <Avatar className="h-8 w-8">
                    <div className="flex h-full w-full items-center justify-center rounded-full bg-primary/10">
                      {stock.symbol[0]}
                    </div>
                  </Avatar>
                  <div>
                    <p className="font-medium">{stock.name}</p>
                    <p className="text-sm text-muted-foreground">{stock.symbol}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-medium">
                    {stock.price} {stock.currency}
                  </p>
                  <p className={Number(stock.change) > 0 ? "text-sm text-green-500" : "text-sm text-red-500"}>
                    {stock.change}%
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
        <div className="mt-4">
          <a href="#" className="text-sm text-blue-500 hover:underline">
            See all stocks with largest daily drop
          </a>
        </div>
      </div>
    </div>
  )
}

