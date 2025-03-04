"use client"

import * as React from "react"
import { Button } from "dashboard/components/ui/button"
import { ScrollArea } from "../../../components/ui/scroll-area"
import { ChevronDown, ChevronRight, FileIcon, FolderIcon, MoreHorizontal, Plus } from "lucide-react"
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

interface FileExplorerProps {
  files: File[]
  onFileSelect: (file: File) => void
}

export function FileExplorer({ files, onFileSelect }: FileExplorerProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between p-2">
        <h2 className="text-sm font-semibold">EXPLORER</h2>
        <Button variant="ghost" size="icon" className="h-6 w-6">
          <Plus className="h-4 w-4" />
        </Button>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-2">
          {files.map((file) => (
            <FileTreeItem key={file.id} file={file} onSelect={onFileSelect} />
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}

function FileTreeItem({ file, onSelect }: { file: File; onSelect: (file: File) => void }) {
  const [isOpen, setIsOpen] = React.useState(true)

  return (
    <div>
      <div className="group flex items-center gap-2 rounded-sm py-1 hover:bg-[#2D2D2D]">
        {file.type === "folder" ? (
          <Button variant="ghost" size="icon" className="h-4 w-4" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
          </Button>
        ) : (
          <div className="w-4" />
        )}
        <div
          className="flex flex-1 items-center gap-2 cursor-pointer"
          onClick={() => file.type === "file" && onSelect(file)}
        >
          {file.type === "folder" ? (
            <FolderIcon className="h-4 w-4 text-[#C5C5C5]" />
          ) : (
            <FileIcon className="h-4 w-4 text-[#C5C5C5]" />
          )}
          <span className="text-sm">{file.name}</span>
        </div>
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
            <FileTreeItem key={child.id} file={child} onSelect={onSelect} />
          ))}
        </div>
      )}
    </div>
  )
}

