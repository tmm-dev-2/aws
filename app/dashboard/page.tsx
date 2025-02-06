"use client"

import { useEffect, useState } from 'react'
import { MarketOverview } from './components/market-overview'
import { NewsPanel } from './components/news-panel'
import { IndexCharts } from './components/index-charts'

export default function Dashboard() {
  const [marketData, setMarketData] = useState(null)
  const [news, setNews] = useState([])
  const [indices, setIndices] = useState(null)

  useEffect(() => {
    fetchMarketData()
    fetchNews()
    fetchIndices()

    const interval = setInterval(() => {
      fetchMarketData()
      fetchIndices()
    }, 60000)

    return () => clearInterval(interval)
  }, [])

  const fetchMarketData = async () => {
    const response = await fetch('http://localhost:5000/market_movers')
    const data = await response.json()
    setMarketData(data)
  }

  const fetchNews = async () => {
    const response = await fetch('http://localhost:5000/market_news')
    const data = await response.json()
    setNews(data.articles)
  }

  const fetchIndices = async () => {
    const response = await fetch('http://localhost:5000/market_indices')
    const data = await response.json()
    setIndices(data)
  }

  return (
    <div className="h-full overflow-auto p-6">
      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-8">
          <IndexCharts data={indices} />
          <div className="mt-6">
            <MarketOverview data={marketData} />
          </div>
        </div>
        <div className="col-span-4">
          <NewsPanel news={news} />
        </div>
      </div>
    </div>
  )
}
