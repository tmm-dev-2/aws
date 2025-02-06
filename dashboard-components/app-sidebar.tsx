"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { BarChart3, ChevronRight, Globe, Menu } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/dashboard-components/ui/sidebar"

const AppSidebar = () => {
  const pathname = usePathname()

  return (
    <Sidebar>
      <SidebarHeader>
        <Link href="/">
          <img src="/logo.svg" alt="logo" className="h-6 w-auto" />
        </Link>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu>
          <SidebarMenuItem href="/" active={pathname === "/"}>
            <BarChart3 className="h-4 w-4 mr-2" />
            Dashboard
          </SidebarMenuItem>
          <SidebarMenuItem href="/profile" active={pathname === "/profile"}>
            <Globe className="h-4 w-4 mr-2" />
            Profile
          </SidebarMenuItem>
          <SidebarMenuSub>
            <SidebarMenuSubButton>
              <Menu className="h-4 w-4 mr-2" />
              More
              <ChevronRight className="h-4 w-4 ml-auto" />
            </SidebarMenuSubButton>
            <SidebarMenuSubItem href="/settings">Settings</SidebarMenuSubItem>
            <SidebarMenuSubItem href="/help">Help</SidebarMenuSubItem>
          </SidebarMenuSub>
        </SidebarMenu>
      </SidebarContent>
    </Sidebar>
  )
}

export default AppSidebar

