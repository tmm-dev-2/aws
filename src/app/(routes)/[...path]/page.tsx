import { DashboardContent } from "@/components/dashboard-content"
import { StockMovers } from "@/components/stock-movers"
import { StockNews } from "@/components/stock-news"

export default function DynamicPage() {
  return (
    <div className="space-y-8">
      <DashboardContent />
      <StockMovers />
      <StockNews />
    </div>
  )
}

