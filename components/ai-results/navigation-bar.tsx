"use client"

import { useState, useMemo } from 'react'

interface PatternData {
  coordinates: number[][]
  analysis: string
  prediction: string
  confidence: number
}

interface NavigationBarProps {
  onPatternSelect: (patternId: string) => void
  patterns: Record<string, PatternData>
}

interface Group {
  name: string
  items: string[]
}

interface SubCategory {
  name: string
  groups: {
    [key: string]: Group
  }
}

interface Category {
  name: string
  subcategories: {
    [key: string]: SubCategory
  }
}

interface Categories {
  [key: string]: Category
}

export const NavigationBar = ({ onPatternSelect, patterns }: NavigationBarProps) => {
  const [searchQuery, setSearchQuery] = useState('')

  const categories: Categories = {
    technical: {
      name: 'Technical Analysis',
      subcategories: {
        patterns: {
          name: 'Patterns',
          groups: {
            candlestick: {
              name: 'Candlestick Patterns',
              items: [
                'bullish_engulfing',
                'bearish_engulfing',
                'hammer',
                'doji',
                'morning_star',
                'evening_star',
                'three_white_soldiers',
                'three_black_crows',
                'piercing_line',
                'dark_cloud_cover'
              ]
            },
            chart: {
              name: 'Chart Patterns',
              items: [
                'double_top',
                'double_bottom',
                'head_and_shoulders',
                'inverse_head_shoulders',
                'ascending_triangle',
                'descending_triangle',
                'symmetrical_triangle',
                'rising_wedge',
                'falling_wedge'
              ]
            }
          }
        },
        indicators: {
          name: 'Technical Indicators',
          groups: {
            trend: {
              name: 'Trend Indicators',
              items: [
                'moving_average',
                'macd',
                'bollinger_bands',
                'parabolic_sar',
                'adx'
              ]
            },
            momentum: {
              name: 'Momentum Indicators',
              items: [
                'rsi',
                'stochastic',
                'cci',
                'williams_r',
                'awesome_oscillator'
              ]
            },
            volume: {
              name: 'Volume Indicators',
              items: [
                'volume',
                'on_balance_volume',
                'money_flow_index',
                'chaikin_money_flow',
                'volume_price_trend'
              ]
            },
            volatility: {
              name: 'Volatility Indicators',
              items: [
                'average_true_range',
                'standard_deviation',
                'historical_volatility',
                'keltner_channels'
              ]
            }
          }
        }
      }
    }
  }

  const filteredCategories = useMemo(() => {
    if (!searchQuery) return categories

    const filtered: Categories = {}
    
    Object.entries(categories).forEach(([catKey, category]) => {
      const matchingSubcats: Record<string, SubCategory> = {}
      
      Object.entries(category.subcategories).forEach(([subKey, subcat]) => {
        const matchingGroups: Record<string, Group> = {}
        
        Object.entries(subcat.groups).forEach(([groupKey, group]) => {
          const matchingItems = group.items.filter(item => 
            item.replace('_', ' ').toLowerCase().includes(searchQuery.toLowerCase())
          )
          
          if (matchingItems.length) {
            matchingGroups[groupKey] = {
              ...group,
              items: matchingItems
            }
          }
        })
        
        if (Object.keys(matchingGroups).length) {
          matchingSubcats[subKey] = {
            ...subcat,
            groups: matchingGroups
          }
        }
      })
      
      if (Object.keys(matchingSubcats).length) {
        filtered[catKey] = {
          ...category,
          subcategories: matchingSubcats
        }
      }
    })
    
    return filtered
  }, [searchQuery])

  return (
    <div className="w-64 bg-[#1E1E1E] border-r border-[#2a2e39] p-4 overflow-auto">
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search patterns..."
          className="w-full bg-[#2a2e39] text-white rounded px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="space-y-4">
        {Object.entries(filteredCategories).map(([catKey, category]) => (
          <div key={catKey}>
            <h3 className="text-gray-400 font-medium mb-2">{category.name}</h3>
            
            {Object.entries(category.subcategories).map(([subKey, subcat]) => (
              <div key={subKey} className="ml-2 mb-3">
                <h4 className="text-gray-500 mb-1">{subcat.name}</h4>
                
                {Object.entries(subcat.groups).map(([groupKey, group]) => (
                  <div key={groupKey} className="ml-2 mb-2">
                    <h5 className="text-gray-500 text-sm mb-1">{group.name}</h5>
                    
                    {group.items.map(item => (
                      <button
                        key={item}
                        className={`block w-full text-left px-2 py-1 rounded text-sm hover:bg-[#2a2e39] transition-colors ${
                          patterns[item] ? 'text-white' : 'text-gray-500'
                        }`}
                        onClick={() => onPatternSelect(item)}
                        disabled={!patterns[item]}
                      >
                        {item.split('_').map(word => 
                          word.charAt(0).toUpperCase() + word.slice(1)
                        ).join(' ')}
                        {patterns[item] && (
                          <span className="ml-2 text-xs text-blue-400">
                            ({patterns[item].coordinates.length})
                          </span>
                        )}
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
