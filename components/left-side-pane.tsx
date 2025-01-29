import { Button } from "components/ui/button"
import { Settings, User, BookOpen, BarChart2, HelpCircle, LayoutDashboard, LineChart } from 'lucide-react'

interface LeftSidePaneProps {
  onAccountClick: () => void;
  onChartClick: () => void;
}

export function LeftSidePane({ onAccountClick, onChartClick }: LeftSidePaneProps) {
  return (
    <div className="w-14 h-full bg-[#1a1a1a] border-r border-[#2a2a2a] flex flex-col items-center py-4 space-y-4">
      <Button variant="ghost" size="icon" className="text-[#666] hover:text-white hover:bg-[#2a2a2a]" title="Dashboard">
        <LayoutDashboard className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="text-[#666] hover:text-white hover:bg-[#2a2a2a]" title="Settings">
        <Settings className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="text-[#666] hover:text-white hover:bg-[#2a2a2a]" title="Chart" onClick={onChartClick}>
        <LineChart className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="text-[#666] hover:text-white hover:bg-[#2a2a2a]" title="Account" onClick={onAccountClick}>
        <User className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="text-[#666] hover:text-white hover:bg-[#2a2a2a]" title="Strategies">
        <BookOpen className="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" className="text-[#666] hover:text-white hover:bg-[#2a2a2a]" title="Performance">
        <BarChart2 className="h-5 w-5" />
      </Button>
      <div className="flex-grow" />
      <Button variant="ghost" size="icon" className="text-[#666] hover:text-white hover:bg-[#2a2a2a]" title="Help">
        <HelpCircle className="h-5 w-5" />
      </Button>
    </div>
  )
}
