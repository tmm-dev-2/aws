import type React from "react"
import { SidebarInset } from "@/components/ui/sidebar"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <SidebarInset>
      <div className="container py-6">{children}</div>
    </SidebarInset>
  )
}

