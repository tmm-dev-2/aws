"use client"
import '../app/globals.css';
import * as React from "react"
import { FileIcon, GitBranch, Search, Settings2, Bug } from "lucide-react"
import { Button } from "dashboard/components/ui/button"
import { ScriptBar } from '../Devscript/editor/components/script-bar'
import { TopBar } from '../Devscript/editor/components/top-bar'
import { ResizablePanel, ResizablePanelGroup, ResizableHandle } from "../components/ui/resizable"
import { FileExplorer } from '../Devscript/editor/components/FileExplorer';
import { CodeEditor } from '../Devscript/editor/components/CodeEditor';
import { TopPanel } from '../Devscript/editor/components/TopPanel';
import { Terminal } from '../Devscript/editor/components/Terminal';

// Initial state types and data
interface File {
  id: string
  name: string
  type: "file" | "folder"
  children?: File[]
}

interface Tab {
  id: string
  name: string
  content: string
}

interface TerminalType {
  id: string
  name: string
  type: "powershell" | "bash" | "node"
  content: string[]
}

const initialFiles: File[] = [
  {
    id: "1",
    name: "app",
    type: "folder",
    children: [
      { id: "2", name: "layout.tsx", type: "file" },
      { id: "3", name: "page.tsx", type: "file" },
    ],
  },
  // Add more initial files as needed
]

export default function Layout() {
  const [files, setFiles] = React.useState<File[]>(initialFiles)
  const [tabs, setTabs] = React.useState<Tab[]>([{ id: "1", name: "layout.tsx", content: "// Your code here" }])
  const [terminals, setTerminals] = React.useState<TerminalType[]>([
    { id: "1", name: "powershell", type: "powershell", content: ["PS C:\\Users\\Admin>"] },
  ])
  const [activeTab, setActiveTab] = React.useState("1")
  const [activeTerminal, setActiveTerminal] = React.useState("1")
  const [showTerminal, setShowTerminal] = React.useState(true)

  const handleNewTerminal = () => {
    const newTerminal: TerminalType = {
      id: String(terminals.length + 1),
      name: "powershell",
      type: "powershell",
      content: ["PS C:\\Users\\Admin>"],
    }
    setTerminals([...terminals, newTerminal])
    setActiveTerminal(newTerminal.id)
  }

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-[#1E1E1E] text-white">
      <ScriptBar />
      <TopBar onToggleTerminal={() => setShowTerminal(!showTerminal)} onNewTerminal={handleNewTerminal} />

      <div className="flex h-[calc(100vh-6rem)]">
        <div className="flex w-12 flex-col items-center border-r border-[#2D2D2D] bg-[#333333] py-2">
          <Button variant="ghost" size="icon" className="mb-2">
            <FileIcon className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <Search className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <GitBranch className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <Bug className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon" className="mt-auto">
            <Settings2 className="h-5 w-5" />
          </Button>
        </div>

        <ResizablePanelGroup direction="horizontal">
          <ResizablePanel defaultSize={20} minSize={15} maxSize={30}>
            <FileExplorer
              files={files}
              onFileSelect={(file) => {
                if (file.type === "file" && !tabs.find((tab) => tab.id === file.id)) {
                  setTabs([...tabs, { id: file.id, name: file.name, content: "// New file content" }])
                  setActiveTab(file.id)
                }
              }}
            />
          </ResizablePanel>

          <ResizableHandle className="bg-[#2D2D2D]" />

          <ResizablePanel defaultSize={60}>
            <ResizablePanelGroup direction="vertical">
              <ResizablePanel defaultSize={70}>
                <CodeEditor
                  tabs={tabs}
                  activeTab={activeTab}
                  onTabChange={setActiveTab}
                  onTabClose={(id) => {
                    setTabs(tabs.filter((tab) => tab.id !== id))
                    if (activeTab === id) {
                      setActiveTab(tabs[0]?.id || "")
                    }
                  }}
                />
              </ResizablePanel>

              {showTerminal && (
                <>
                  <ResizableHandle className="bg-[#2D2D2D]" />
                  <ResizablePanel defaultSize={30}>
                    <Terminal
                      terminals={terminals}
                      activeTerminal={activeTerminal}
                      onTerminalChange={setActiveTerminal}
                      onNewTerminal={handleNewTerminal}
                      onClose={() => setShowTerminal(false)}
                    />
                  </ResizablePanel>
                </>
              )}
            </ResizablePanelGroup>
          </ResizablePanel>

          <ResizableHandle className="bg-[#2D2D2D]" />

          <ResizablePanel defaultSize={20} minSize={15} maxSize={30}>
          </ResizablePanel>
        </ResizablePanelGroup>
      </div>
    </div>
  )
}

