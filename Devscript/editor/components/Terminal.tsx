"use client"
import { Button } from "dashboard/components/ui/button"
import { ScrollArea } from "../../../components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "dashboard/components/ui/tabs"
import { Plus, TerminalIcon } from "lucide-react"

interface Terminal {
  id: string
  name: string
  type: "powershell" | "bash" | "node"
  content: string[]
}

interface TerminalProps {
  terminals: Terminal[]
  activeTerminal: string
  onTerminalChange: (id: string) => void
  onNewTerminal: () => void
  onClose: () => void
}

export function Terminal({ terminals, activeTerminal, onTerminalChange, onNewTerminal, onClose }: TerminalProps) {
  return (
    <div className="flex h-full flex-col bg-[#1E1E1E]">
      <Tabs value={activeTerminal} onValueChange={onTerminalChange}>
        <div className="flex items-center justify-between border-b border-[#2D2D2D] bg-[#2D2D2D]">
          <TabsList className="bg-transparent">
            {terminals.map((term) => (
              <TabsTrigger key={term.id} value={term.id} className="data-[state=active]:bg-[#1E1E1E]">
                <TerminalIcon className="mr-1 h-3 w-3" />
                {term.name}
              </TabsTrigger>
            ))}
          </TabsList>
          <div className="flex items-center px-2">
            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={onNewTerminal}>
              <Plus className="h-3 w-3" />
            </Button>
            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={onClose}>
              ×
            </Button>
          </div>
        </div>
        {terminals.map((term) => (
          <TabsContent key={term.id} value={term.id} className="h-full">
            <ScrollArea className="h-full border-0 p-4">
              {term.content.map((line, i) => (
                <div key={i} className="font-mono text-sm text-white">
                  {line}
                </div>
              ))}
            </ScrollArea>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  )
}

