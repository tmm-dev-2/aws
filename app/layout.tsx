import type { Metadata } from "next"
import { Inter } from 'next/font/google'
import "./globals.css"
import { Providers } from './providers';

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Stock Charts & Alerts",
  description: "Real-time stock charts and price alerts",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
