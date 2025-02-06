import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export function IndexCharts({ data }) {
  if (!data) return null

  return (
    <div className="bg-[#252526] rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Market Indices</h2>
      <div className="grid grid-cols-2 gap-4">
        {Object.entries(data).map(([index, indexData]: [string, any]) => (
          <div key={index} className="h-[200px]">
            <h3 className="text-sm mb-2">
              {index.replace('^', '')} 
              <span className={indexData.change > 0 ? 'text-green-500' : 'text-red-500'}>
                {indexData.changePercent.toFixed(2)}%
              </span>
            </h3>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={indexData.prices.map((price, i) => ({
                price,
                time: indexData.times[i]
              }))}>
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke={indexData.change > 0 ? '#22c55e' : '#ef4444'} 
                  dot={false}
                />
                <XAxis dataKey="time" />
                <YAxis domain={['auto', 'auto']} />
                <Tooltip />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ))}
      </div>
    </div>
  )
}
