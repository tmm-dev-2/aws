export function TopNav() {
  return (
    <nav className="flex items-center space-x-6 text-sm">
      <div className="flex items-center space-x-4">
        <span className="hover:text-blue-400 cursor-pointer">Products</span>
        <span className="hover:text-blue-400 cursor-pointer">Markets</span>
        <span className="hover:text-blue-400 cursor-pointer">Screener</span>
        <span className="hover:text-blue-400 cursor-pointer">Community</span>
        <span className="hover:text-blue-400 cursor-pointer">Features</span>
      </div>
      <div className="flex-1" />
      <div className="flex items-center space-x-4">
        <span className="hover:text-blue-400 cursor-pointer">Get Started</span>
        <span className="hover:text-blue-400 cursor-pointer">Upgrade</span>
      </div>
    </nav>
  )
}
