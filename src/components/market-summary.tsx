"use client"

import { Card } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const indices = [
  {
    name: "Nifty 50",
    value: "23,482.15",
    change: "-0.11%",
    currency: "INR",
    isNegative: true,
  },
  {
    name: "Sensex",
    value: "77,505.96",
    change: "+0.01%",
    currency: "INR",
    isNegative: false,
  },
  {
    name: "S&P 500",
    value: "6,040.52",
    change: "-0.51%",
    currency: "USD",
    isNegative: true,
  },
  {
    name: "Nasdaq 100",
    value: "21,478.05",
    change: "-0.14%",
    currency: "USD",
    isNegative: true,
  },
]

export function MarketSummary() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold tracking-tight">Market summary</h2>
      </div>
      <Tabs defaultValue="indices" className="space-y-4">
        <TabsList>
          <TabsTrigger value="indices">Indices</TabsTrigger>
          <TabsTrigger value="stocks">Stocks</TabsTrigger>
          <TabsTrigger value="crypto">Crypto</TabsTrigger>
          <TabsTrigger value="futures">Futures</TabsTrigger>
          <TabsTrigger value="forex">Forex</TabsTrigger>
          <TabsTrigger value="bonds">Bonds</TabsTrigger>
          <TabsTrigger value="etfs">ETFs</TabsTrigger>
        </TabsList>
        <TabsContent value="indices" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {indices.map((index) => (
              <Card key={index.name} className="p-4">
                <div className="space-y-2">
                  <p className="text-sm font-medium leading-none">{index.name}</p>
                  <p className="text-2xl font-bold">
                    {index.value}
                    <span className="text-xs font-normal text-muted-foreground">{index.currency}</span>
                  </p>
                  <p
                    className={
                      index.isNegative ? "text-sm font-medium text-red-500" : "text-sm font-medium text-green-500"
                    }
                  >
                    {index.change}
                  </p>
                </div>
              </Card>
            ))}
          </div>
          <Card className="h-[400px] w-full">
            <div className="h-full w-full bg-muted/20">
              {/* Placeholder for chart */}
              <div className="flex h-full items-center justify-center">
                <p className="text-muted-foreground">Chart placeholder</p>
              </div>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

