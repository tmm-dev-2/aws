"use client"

import * as React from "react"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "../../../components/ui/resizable"
import { ScrollArea } from "../../../components/ui/scroll-area"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "dashboard/components/ui/tabs"
import { cn } from "dashboard/lib/utils"
import {
  ChevronDown,
  FileIcon,
  FolderIcon,
  MoreHorizontal,
  Plus,
  Settings,
  TerminalIcon,
  Save,
  ChevronRight,
  ExternalLink,
  HelpCircle,
  LineChart,
  Library,
} from "lucide-react"
import { Button } from "dashboard/components/ui/button"
import { Input } from "dashboard/components/ui/input"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../../../components/ui/dropdown-menu"

interface File {
  id: string
  name: string
  type: "file" | "folder"
  children?: File[]
}

const initialFiles: File[] = [
  {
    id: "1",
    name: "app",
    type: "folder",
    children: [
      {
        id: "2",
        name: "layout.tsx",
        type: "file",
      },
      {
        id: "3",
        name: "page.tsx",
        type: "file",
      },
    ],
  },
  {
    id: "4",
    name: "components",
    type: "folder",
    children: [
      {
        id: "5",
        name: "ui",
        type: "folder",
        children: [
          {
            id: "6",
            name: "button.tsx",
            type: "file",
          },
          {
            id: "7",
            name: "dialog.tsx",
            type: "file",
          },
        ],
      },
    ],
  },
]

interface Tab {
  id: string
  name: string
  content: string
}

interface Terminal {
  id: string
  name: string
  type: "powershell" | "bash" | "cmd"
  content: string[]
}

export default function Layout() {
  const [files, setFiles] = React.useState<File[]>(initialFiles)
  const [tabs, setTabs] = React.useState<Tab[]>([
    {
      id: "1",
      name: "layout.tsx",
      content: "// Your code here",
    },
  ])
  const [terminals, setTerminals] = React.useState<Terminal[]>([
    {
      id: "1",
      name: "powershell",
      type: "powershell",
      content: ["PS C:\\Users\\Admin>"],
    },
  ])
  const [activeTab, setActiveTab] = React.useState("1")
  const [activeTerminal, setActiveTerminal] = React.useState("1")
  const [showTerminal, setShowTerminal] = React.useState(true)

  const addNewTerminal = (type: Terminal["type"]) => {
    const newTerminal: Terminal = {
      id: String(terminals.length + 1),
      name: type,
      type,
      content: [type === "powershell" ? "PS C:\\Users\\Admin>" : "$"],
    }
    setTerminals([...terminals, newTerminal])
    setActiveTerminal(newTerminal.id)
  }

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-[#1E1E1E] text-white">
      {/* Script Management Bar */}
      <div className="flex h-8 items-center justify-between border-b border-[#2D2D2D] bg-[#1E1E1E] px-4">
        <div className="flex items-center gap-2">
          <span className="text-sm">Untitled script</span>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs">
            <Save className="mr-1 h-3 w-3" />
            Save
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-6 w-6">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-48">
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                Editor settings
              </DropdownMenuItem>
              <DropdownMenuItem>
                <ExternalLink className="mr-2 h-4 w-4" />
                Open in new window
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <LineChart className="mr-2 h-4 w-4" />
                Pine logs
              </DropdownMenuItem>
              <DropdownMenuItem>
                <HelpCircle className="mr-2 h-4 w-4" />
                Help
              </DropdownMenuItem>
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

      {/* Top Menu Bar */}
      <div className="flex h-10 items-center border-b border-[#2D2D2D] px-4">
        <div className="flex space-x-4">
          {["File", "Edit", "Selection", "View", "Go", "Run", "Terminal", "Help"].map((item) => (
            <Button
              key={item}
              variant="ghost"
              className="px-2 py-1 text-sm hover:bg-[#2D2D2D]"
              onClick={() => {
                if (item === "Terminal") {
                  setShowTerminal(true)
                  addNewTerminal("powershell")
                }
              }}
            >
              {item}
            </Button>
          ))}
        </div>
      </div>

      <ResizablePanelGroup direction="horizontal">
        {/* File Explorer */}
        <ResizablePanel defaultSize={20} minSize={15} maxSize={30}>
          <div className="flex h-full flex-col">
            <div className="flex items-center justify-between p-2">
              <h2 className="text-sm font-semibold">EXPLORER</h2>
              <Button variant="ghost" size="icon" className="h-6 w-6">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            <ScrollArea className="flex-1">
              <FileTree files={files} />
            </ScrollArea>
          </div>
        </ResizablePanel>

        <ResizableHandle className="bg-[#2D2D2D]" />

        {/* Main Editor Area */}
        <ResizablePanel defaultSize={60}>
          <ResizablePanelGroup direction="vertical">
            <ResizablePanel defaultSize={70}>
              <div className="flex h-full flex-col">
                {/* Tabs */}
                <div className="flex border-b">
                  {tabs.map((tab) => (
                    <div
                      key={tab.id}
                      className={cn(
                        "flex items-center gap-2 border-r px-4 py-2",
                        activeTab === tab.id ? "bg-background" : "bg-muted/30 hover:bg-muted/50",
                      )}
                    >
                      <FileIcon className="h-4 w-4" />
                      <span className="text-sm">{tab.name}</span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-4 w-4 opacity-0 group-hover:opacity-100"
                        onClick={() => {
                          setTabs(tabs.filter((t) => t.id !== tab.id))
                          if (activeTab === tab.id) {
                            setActiveTab(tabs[0]?.id || "")
                          }
                        }}
                      >
                        ×
                      </Button>
                    </div>
                  ))}
                </div>

                {/* Editor Content */}
                <div className="flex-1 p-4">
                  <pre className="text-sm">
                    <code>{tabs.find((tab) => tab.id === activeTab)?.content}</code>
                  </pre>
                </div>
              </div>
            </ResizablePanel>

            <ResizableHandle className="bg-[#2D2D2D]" />

            {/* Terminal Panel with Tabs */}
            {showTerminal && (
              <ResizablePanel defaultSize={30}>
                <div className="flex h-full flex-col bg-[#1E1E1E]">
                  <Tabs value={activeTerminal} onValueChange={setActiveTerminal}>
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
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6"
                          onClick={() => addNewTerminal("powershell")}
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                        <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setShowTerminal(false)}>
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
              </ResizablePanel>
            )}
          </ResizablePanelGroup>
        </ResizablePanel>

        <ResizableHandle className="bg-[#2D2D2D]" />

        {/* AI Assistant Panel */}
        <ResizablePanel defaultSize={20} minSize={15} maxSize={30}>
          <div className="flex h-full flex-col">
            <div className="flex items-center justify-between border-b p-2">
              <h2 className="text-sm font-semibold">AI ASSISTANT</h2>
              <Button variant="ghost" size="icon" className="h-6 w-6">
                <Settings className="h-4 w-4" />
              </Button>
            </div>
            <ScrollArea className="flex-1 p-4">
              <div className="space-y-4">
                <div className="rounded-lg border bg-muted/50 p-4">
                  <h3 className="mb-2 text-sm font-medium">How can I help you?</h3>
                  <p className="text-sm text-muted-foreground">
                    Ask me about your code, debugging, or any programming questions.
                  </p>
                </div>
                <Input placeholder="Type your question..." />
              </div>
            </ScrollArea>
          </div>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  )
}

function FileTree({ files }: { files: File[] }) {
  return (
    <div className="p-2">
      {files.map((file) => (
        <FileTreeItem key={file.id} file={file} />
      ))}
    </div>
  )
}

function FileTreeItem({ file }: { file: File }) {
  const [isOpen, setIsOpen] = React.useState(true)

  return (
    <div>
      <div className="group flex items-center gap-2 rounded-sm py-1 hover:bg-muted/50">
        {file.type === "folder" ? (
          <Button variant="ghost" size="icon" className="h-4 w-4" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
          </Button>
        ) : (
          <div className="w-4" />
        )}
        {file.type === "folder" ? (
          <FolderIcon className="h-4 w-4 text-muted-foreground" />
        ) : (
          <FileIcon className="h-4 w-4 text-muted-foreground" />
        )}
        <span className="text-sm">{file.name}</span>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="h-4 w-4 opacity-0 group-hover:opacity-100">
              <MoreHorizontal className="h-3 w-3" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start">
            <DropdownMenuItem>New File</DropdownMenuItem>
            <DropdownMenuItem>New Folder</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Copy</DropdownMenuItem>
            <DropdownMenuItem>Cut</DropdownMenuItem>
            <DropdownMenuItem className="text-red-600">Delete</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      {file.type === "folder" && isOpen && file.children && (
        <div className="ml-4">
          {file.children.map((child) => (
            <FileTreeItem key={child.id} file={child} />
          ))}
        </div>
      )}
    </div>
  )
}

