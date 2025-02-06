export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex flex-col h-screen bg-[#1E1E1E]">
      <div className="h-12 border-b border-[#2a2a2a] flex items-center px-4">
        <TopNav />
      </div>
      {children}
    </div>
  )
}
