"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { BarChart3, ChevronRight, Globe, Menu } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "dashboard/components/ui/sidebar"

const menuItems = [
  {
    title: "Market summary",
    icon: BarChart3,
    href: "/market-summary",
    submenu: [
      { title: "Overview", href: "/market-summary/overview" },
      { title: "Stocks", href: "/market-summary/stocks" },
      { title: "Crypto", href: "/market-summary/crypto" },
      { title: "Futures", href: "/market-summary/futures" },
      { title: "Forex", href: "/market-summary/forex" },
      { title: "Government bonds", href: "/market-summary/government-bonds" },
      { title: "Corporate bonds", href: "/market-summary/corporate-bonds" },
      { title: "ETFs", href: "/market-summary/etfs" },
    ],
  },
  {
    title: "Indian stocks",
    icon: Globe,
    href: "/indian-stocks",
  },
  {
    title: "World stocks",
    icon: Globe,
    href: "/world-stocks",
  },
  {
    title: "Community",
    icon: Globe,
    href: "/community",
  },
  {
    title: "Brokers",
    icon: Globe,
    href: "/brokers",
  },
]

export function AppSidebar() {
  const pathname = usePathname()

  return (
    <Sidebar>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg">
              <Menu className="h-6 w-6" />
              <span className="font-semibold">TradingView</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu>
          {menuItems.map((item) => (
            <React.Fragment key={item.title}>
              {item.submenu ? (
                <SidebarMenuItem>
                  <SidebarMenuButton>
                    <item.icon className="h-4 w-4" />
                    <span>{item.title}</span>
                    <ChevronRight className="ml-auto h-4 w-4" />
                  </SidebarMenuButton>
                  <SidebarMenuSub>
                    {item.submenu.map((subItem) => (
                      <SidebarMenuSubItem key={subItem.title}>
                        <SidebarMenuSubButton asChild isActive={pathname === subItem.href}>
                          <Link href={subItem.href}>{subItem.title}</Link>
                        </SidebarMenuSubButton>
                      </SidebarMenuSubItem>
                    ))}
                  </SidebarMenuSub>
                </SidebarMenuItem>
              ) : (
                <SidebarMenuItem>
                  <SidebarMenuButton asChild isActive={pathname === item.href}>
                    <Link href={item.href}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              )}
            </React.Fragment>
          ))}
        </SidebarMenu>
      </SidebarContent>
    </Sidebar>
  )
}

