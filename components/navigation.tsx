import { Home, LineChart, Bell, Settings } from 'lucide-react'
import { Button } from "dashboard/components/ui/button"

export function Navigation() {
  return (
    <div className="p-6 space-y-4">
      <h2 className="text-lg font-semibold mb-6">StockChart</h2>
      <div className="space-y-2">
        <Button variant="ghost" className="w-full justify-start button">
          <Home className="mr-2 h-4 w-4" />
          Dashboard
        </Button>
        <Button variant="ghost" className="w-full justify-start button">
          <LineChart className="mr-2 h-4 w-4" />
          Charts
        </Button>
        <Button variant="ghost" className="w-full justify-start button">
          <Bell className="mr-2 h-4 w-4" />
          Alerts
        </Button>
        <Button variant="ghost" className="w-full justify-start button">
          <Settings className="mr-2 h-4 w-4" />
          Settings
        </Button>
      </div>
    </div>
  )
}

