"use client"
import { Button } from "dashboard/components/ui/button"
import { Input } from "dashboard/components/ui/input"
import { ScrollArea } from "../components/ui/scroll-area"
import { Settings2 } from "lucide-react"

export function AiAssistant() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-[#2D2D2D] p-2">
        <h2 className="text-sm font-semibold">AI ASSISTANT</h2>
        <Button variant="ghost" size="icon" className="h-6 w-6">
          <Settings2 className="h-4 w-4" />
        </Button>
      </div>
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4">
          <div className="rounded-lg border border-[#2D2D2D] bg-[#2D2D2D] p-4">
            <h3 className="mb-2 text-sm font-medium">How can I help you?</h3>
            <p className="text-sm text-muted-foreground">
              Ask me about your code, debugging, or any programming questions.
            </p>
          </div>
          <Input placeholder="Type your question..." className="bg-[#3C3C3C]" />
        </div>
      </ScrollArea>
    </div>
  )
}

