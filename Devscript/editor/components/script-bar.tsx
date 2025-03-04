"use client"
import { Library, MoreHorizontal, Save } from "lucide-react"
import { Button } from "../../../components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../../../components/ui/dropdown-menu"


export function ScriptBar() {
  return (
    <div className="flex h-8 items-center justify-between border-b border-[#2D2D2D] bg-[#1E1E1E] px-4">
      <div className="flex items-center gap-2">
        <div className="flex flex-col">
          <span className="text-sm text-white">Untitled script</span>
          <span className="text-xs text-blue-400">Save</span>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start">
            <DropdownMenuItem>
              <Save className="mr-2 h-4 w-4" />
              Save script
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Make a copy...</DropdownMenuItem>
            <DropdownMenuItem>Rename...</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="sm" className="h-6 px-2">
          Add to chart
        </Button>
        <Button variant="ghost" size="sm" className="h-6 px-2 text-blue-400">
          <Library className="mr-1 h-3 w-3" />
          Publish library
        </Button>
        <Button variant="ghost" size="icon" className="h-6 w-6">
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

