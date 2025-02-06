"use client"

import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const indicators = [
  {
    title: "Asset Rotation System [InvestorUnknown]",
    description:
      "Overview This system creates a comprehensive trend 'matrix' by analyzing the performance of six assets against both the US Dollar and each other.",
    author: "InvestorUnknown",
    date: "Updated Jan 31",
    comments: 11,
    likes: 407,
  },
  {
    title: "TASC 2025.02 Autocorrelation Indicator",
    description:
      "OVERVIEW This script implements the Autocorrelation Indicator introduced by John Ehlers in the 'Drunkard's Walk: Theory And Measurement By Autocorrelation'",
    author: "PineCodersTASC",
    date: "Jan 20",
    comments: 4,
    likes: 234,
  },
  {
    title: "Session Bar/Candle Coloring",
    description:
      "Change the color of candles within a user-defined trading session. Borders and wicks can be changed as well, not just the body color.",
    author: "n00btraders",
    date: "Jan 14",
    comments: 8,
    likes: 355,
  },
]

export function IndicatorsStrategies() {
  return (
    <Tabs defaultValue="editors-picks" className="mt-4">
      <TabsList>
        <TabsTrigger value="editors-picks">Editors&apos; picks</TabsTrigger>
        <TabsTrigger value="following">Following</TabsTrigger>
        <TabsTrigger value="popular">Popular</TabsTrigger>
      </TabsList>
      <TabsContent value="editors-picks" className="mt-4">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {indicators.map((indicator) => (
            <Card key={indicator.title} className="overflow-hidden">
              <div className="aspect-[4/3] bg-muted/20">
                {/* Placeholder for indicator visualization */}
                <div className="flex h-full items-center justify-center">
                  <p className="text-muted-foreground">Indicator placeholder</p>
                </div>
              </div>
              <CardHeader className="p-4">
                <h3 className="line-clamp-2 text-base font-semibold">{indicator.title}</h3>
                <p className="line-clamp-2 text-sm text-muted-foreground">{indicator.description}</p>
              </CardHeader>
              <CardContent className="flex items-center justify-between p-4 pt-0">
                <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                  <span>{indicator.author}</span>
                  <span>•</span>
                  <span>{indicator.date}</span>
                </div>
                <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                  <span>{indicator.comments} 💬</span>
                  <span>{indicator.likes} 👍</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </TabsContent>
    </Tabs>
  )
}

