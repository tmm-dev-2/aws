import React, { useState } from 'react'
import { Button } from "dashboard/components/ui/button"
import { 
  Crosshair, 
  Move, 
  ZoomIn, 
  PenLine, 
  Eraser, 
  ChevronLeft, 
  ChevronRight,
  LineChart,
  Square,
  Circle,
  Triangle,
  ArrowRight,
  Ruler,
  Type,
  Scissors,
  Magnet,
  Edit,
  Baseline,
  FoldHorizontal,
  MoreHorizontal,
  Minimize2
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

// Comprehensive list of TradingView-like drawing tools
export const DRAWING_TOOLS = [
  {
    category: 'Trend Lines',
    tools: [
      { icon: LineChart, name: "Trend Line", value: "trendline" },
      { icon: Baseline, name: "Horizontal Line", value: "horizontal" },
      { icon: FoldHorizontal, name: "Parallel Channel", value: "channel" },
      { icon: MoreHorizontal, name: "Pitchfork", value: "pitchfork" },
    ]
  },
  {
    category: 'Shapes',
    tools: [
      { icon: Square, name: "Rectangle", value: "rectangle" },
      { icon: Circle, name: "Ellipse", value: "ellipse" },
      { icon: Triangle, name: "Triangle", value: "triangle" },
    ]
  },
  {
    category: 'Annotations',
    tools: [
      { icon: Type, name: "Text", value: "text" },
      { icon: Edit, name: "Note", value: "note" },
    ]
  },
  {
    category: 'Advanced',
    tools: [
      { icon: ArrowRight, name: "Arrow", value: "arrow" },
      { icon: Ruler, name: "Measure", value: "measure" },
      { icon: Magnet, name: "Magnet", value: "magnet" },
    ]
  }
]

export function ChartTools() {
  const [selectedTool, setSelectedTool] = useState<string | null>(null)
  const [isDrawingMode, setIsDrawingMode] = useState(false)
  const [isDrawingToolsOpen, setIsDrawingToolsOpen] = useState(false)

  const handleToolSelect = (tool: string) => {
    setSelectedTool(tool)
    setIsDrawingMode(true)
    setIsDrawingToolsOpen(false)
    
    // Dispatch custom event to notify chart of tool selection
    window.dispatchEvent(new CustomEvent('drawingToolChange', { 
      detail: { tool, isDrawingMode: true } 
    }))
  }

  const toggleDrawingMode = () => {
    const newDrawingMode = !isDrawingMode
    setIsDrawingMode(newDrawingMode)
    
    window.dispatchEvent(new CustomEvent('drawingModeToggle', { 
      detail: { isDrawingMode: newDrawingMode } 
    }))
  }

  const resetTool = () => {
    setSelectedTool(null)
    setIsDrawingMode(false)
    
    window.dispatchEvent(new CustomEvent('drawingToolReset'))
  }

  return (
    <div className="border-r border-border p-2 flex flex-col items-center justify-between h-full">
      <div className="space-y-4">
        <Button 
          variant={selectedTool === 'crosshair' ? "default" : "ghost"} 
          size="icon" 
          title="Crosshair" 
          className="button"
          onClick={() => handleToolSelect('crosshair')}
        >
          <Crosshair className="h-4 w-4" />
        </Button>
        <Button 
          variant={selectedTool === 'move' ? "default" : "ghost"} 
          size="icon" 
          title="Move" 
          className="button"
          onClick={() => handleToolSelect('move')}
        >
          <Move className="h-4 w-4" />
        </Button>
        <Button 
          variant={selectedTool === 'zoom' ? "default" : "ghost"} 
          size="icon" 
          title="Zoom" 
          className="button"
          onClick={() => handleToolSelect('zoom')}
        >
          <ZoomIn className="h-4 w-4" />
        </Button>
        
        <DropdownMenu open={isDrawingToolsOpen} onOpenChange={setIsDrawingToolsOpen}>
          <DropdownMenuTrigger asChild>
            <Button 
              variant={selectedTool && isDrawingMode ? "default" : "ghost"} 
              size="icon" 
              title="Drawing Tools" 
              className="button"
            >
              <PenLine className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-64">
            {DRAWING_TOOLS.map((category) => (
              <DropdownMenuSub key={category.category}>
              <DropdownMenuSubTrigger>{category.category}</DropdownMenuSubTrigger>
              <DropdownMenuSubContent>
                {category.tools.map((tool) => (
                <DropdownMenuItem 
                  key={tool.value} 
                  onSelect={() => handleToolSelect(tool.value)}
                  className="cursor-pointer"
                >
                  <tool.icon className="mr-2 h-4 w-4" />
                  {tool.name}
                </DropdownMenuItem>
                ))}
              </DropdownMenuSubContent>
              </DropdownMenuSub>
            ))}
            </DropdownMenuContent>

        </DropdownMenu>

        <Button 
          variant={selectedTool === 'erase' ? "default" : "ghost"} 
          size="icon" 
          title="Erase" 
          className="button"
          onClick={() => handleToolSelect('erase')}
        >
          <Eraser className="h-4 w-4" />
        </Button>
        <Button 
          variant="ghost" 
          size="icon" 
          title="Reset" 
          className="button"
          onClick={resetTool}
        >
          <Minimize2 className="h-4 w-4" />
        </Button>
      </div>
      <div className="space-y-4">
        <Button variant="ghost" size="icon" title="Previous" className="button">
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <Button variant="ghost" size="icon" title="Next" className="button">
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}