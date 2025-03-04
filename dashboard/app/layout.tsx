import { SidebarProvider } from "dashboard/components/ui/sidebar"
import { AppSidebar } from "dashboard/components/app-sidebar"
import type React from "react" // Added import for React

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body>
        <SidebarProvider>
          <div className="flex min-h-screen bg-background">
            <AppSidebar />
            <main className="flex-1">{children}</main>
          </div>
        </SidebarProvider>
      </body>
    </html>
  )
}

