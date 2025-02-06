"use client"
import { MarketSummary } from "@/dashboard-components/market-summary"
import { CommunityIdeas } from "@/dashboard-components/community-ideas"
import { IndicatorsStrategies } from "@/dashboard-components/indicators-strategies"
import { TopStories } from "@/dashboard-components/top-stories"
import { TradeIdeas } from "@/dashboard-components/trade-ideas"
import { CommunityTrends } from "@/dashboard-components/community-trends"
import { StockMovers } from "@/dashboard-components/stock-movers"
import { StockNews } from "@/dashboard-components/stock-news"

export function DashboardContent() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <MarketSummary />
      <CommunityIdeas />
      <IndicatorsStrategies />
      <TopStories />
      <TradeIdeas />
      <CommunityTrends />
      <StockMovers />
      <StockNews />
    </div>
  )
}

