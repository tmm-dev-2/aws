"use client"

import { ChevronRight, Search } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { MarketSummary } from "@/components/market-summary"
import { CommunityIdeas } from "@/components/community-ideas"
import { IndicatorsStrategies } from "@/components/indicators-strategies"
import { TopStories } from "@/components/top-stories"
import { TradeIdeas } from "@/components/trade-ideas"
import { CommunityTrends } from "@/components/community-trends"
import { StockMovers } from "@/components/stock-movers"
import { StockNews } from "@/components/stock-news"

export function DashboardContent() {
  return (
    <div className="container py-6 space-y-8">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-14 items-center">
          <div className="flex flex-1 items-center space-x-2">
            <div className="w-full max-w-xl">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input type="search" placeholder="Search (Ctrl+K)" className="pl-8" />
              </div>
            </div>
            <nav className="flex items-center space-x-6">
              <Link href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
                Products
              </Link>
              <Link href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
                Community
              </Link>
              <Link href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
                Markets
              </Link>
              <Link href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
                News
              </Link>
            </nav>
            <div className="ml-auto flex items-center space-x-4">
              <Button variant="outline">Sign In</Button>
              <Button>Get Started</Button>
            </div>
          </div>
        </div>
      </header>

      <MarketSummary />

      <section>
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold tracking-tight">
            Community ideas
            <ChevronRight className="ml-1 inline-block h-6 w-6" />
          </h2>
        </div>
        <CommunityIdeas />
      </section>

      <section>
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold tracking-tight">
            Indicators and strategies
            <ChevronRight className="ml-1 inline-block h-6 w-6" />
          </h2>
        </div>
        <IndicatorsStrategies />
      </section>

      <section>
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold tracking-tight">
            Top stories
            <ChevronRight className="ml-1 inline-block h-6 w-6" />
          </h2>
        </div>
        <TopStories />
      </section>

      <StockMovers />

      <StockNews />

      <section>
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold tracking-tight">
            Indian stocks
            <ChevronRight className="ml-1 inline-block h-6 w-6" />
          </h2>
        </div>
        <TradeIdeas />
      </section>

      <section>
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold tracking-tight">Community trends</h2>
        </div>
        <CommunityTrends />
      </section>
    </div>
  )
}

