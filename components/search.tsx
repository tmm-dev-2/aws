"use client"

import { SearchIcon } from 'lucide-react'
import { Input } from "dashboard/components/ui/input"

export function Search() {
  return (
    <div className="relative">
      <SearchIcon className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input placeholder="Search stocks..." className="pl-8" />
    </div>
  )
}

