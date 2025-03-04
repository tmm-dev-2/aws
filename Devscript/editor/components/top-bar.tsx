"use client"
import { Button } from "dashboard/components/ui/button"
import { Input } from "dashboard/components/ui/input"
import { Search } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../../../components/ui/dropdown-menu"

interface TopBarProps {
  onToggleTerminal: () => void
  onNewTerminal: () => void
}

export function TopBar({ onToggleTerminal, onNewTerminal }: TopBarProps) {
  const menuItems = ["File", "Edit", "Selection", "View", "Go", "Run", "Terminal", "Help"]

  return (
    <div className="flex h-10 items-center justify-between border-b border-[#2D2D2D] px-4">
      <div className="flex items-center space-x-4">
        {menuItems.map((item) => (
          <DropdownMenu key={item}>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="px-2 py-1 text-sm hover:bg-[#2D2D2D]"
                onClick={() => {
                  if (item === "Terminal") {
                    onToggleTerminal()
                    onNewTerminal()
                  }
                }}
              >
                {item}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem>New File</DropdownMenuItem>
              <DropdownMenuItem>Open File...</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Save</DropdownMenuItem>
              <DropdownMenuItem>Save As...</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        ))}
      </div>
      <div className="flex items-center space-x-2">
        <Input
          className="h-6 w-64 bg-[#3C3C3C] text-sm"
          placeholder="Search files..."
          startContent={<Search className="h-3 w-3" />}
        />
      </div>
    </div>
  )
}

