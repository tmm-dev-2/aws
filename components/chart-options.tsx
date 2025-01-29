import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export function ChartOptions() {
  return (
    <div className="flex items-center justify-between p-4 border-b border-border">
      <div className="flex space-x-2">
        <Button variant="outline" size="sm" className="button">1D</Button>
        <Button variant="outline" size="sm" className="button">1W</Button>
        <Button variant="outline" size="sm" className="button">1M</Button>
        <Button variant="outline" size="sm" className="button">3M</Button>
        <Button variant="outline" size="sm" className="button">1Y</Button>
        <Button variant="outline" size="sm" className="button">5Y</Button>
      </div>
      <div className="flex items-center space-x-4">
        <Select defaultValue="candles">
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Chart Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="candles">Candlesticks</SelectItem>
            <SelectItem value="bar">Bar Chart</SelectItem>
            <SelectItem value="line">Line Chart</SelectItem>
          </SelectContent>
        </Select>
        <Select>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Algo Strategy" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="moving-average">Moving Average</SelectItem>
            <SelectItem value="rsi">RSI</SelectItem>
            <SelectItem value="macd">MACD</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  )
}

