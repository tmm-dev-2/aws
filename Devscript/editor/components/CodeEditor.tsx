"use client"
import { FileIcon } from "lucide-react"
import { Button } from "dashboard/components/ui/button"
import { cn } from "dashboard/lib/utils"

interface Tab {
  id: string
  name: string
  content: string
}

interface CodeEditorProps {
  tabs: Tab[]
  activeTab: string
  onTabChange: (id: string) => void
  onTabClose: (id: string) => void
}

export function CodeEditor({ tabs, activeTab, onTabChange, onTabClose }: CodeEditorProps) {
  return (
    <div className="flex h-full flex-col">
      {/* Tabs */}
      <div className="flex border-b border-[#2D2D2D]">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={cn(
              "group flex items-center gap-2 border-r border-[#2D2D2D] px-4 py-2",
              activeTab === tab.id ? "bg-[#1E1E1E]" : "bg-[#2D2D2D] hover:bg-[#3C3C3C]",
            )}
          >
            <FileIcon className="h-4 w-4" />
            <span className="text-sm">{tab.name}</span>
            <Button
              variant="ghost"
              size="icon"
              className="h-4 w-4 opacity-0 group-hover:opacity-100"
              onClick={() => onTabClose(tab.id)}
            >
              ×
            </Button>
          </div>
        ))}
      </div>

      {/* Editor Content */}
      <div className="flex-1 p-4">
        <pre className="font-mono text-sm">
          <code>{tabs.find((tab) => tab.id === activeTab)?.content}</code>
        </pre>
      </div>
    </div>
  )
}

