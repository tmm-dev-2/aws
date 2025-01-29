import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus } from 'lucide-react'

export function Lists() {
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="pb-4">
          <CardTitle className="text-sm font-medium">Tech Stocks</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">AAPL, GOOGL, MSFT, AMZN</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="pb-4">
          <CardTitle className="text-sm font-medium">Watchlist</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">TSLA, NVDA, AMD</p>
        </CardContent>
      </Card>
      <Button variant="outline" className="w-full button">
        <Plus className="mr-2 h-4 w-4" /> Create New List
      </Button>
    </div>
  )
}

