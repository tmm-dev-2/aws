import { DashboardContent } from "dashboard/components/dashboard-content"
import { StockMovers } from "dashboard/components/stock-movers"
import { StockNews } from "dashboard/components/stock-news"

export default function DynamicPage() {
  return (
    <div className="space-y-8">
      <DashboardContent />
      <StockMovers />
      <StockNews />
    </div>
  )
}

