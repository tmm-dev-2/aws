"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts"
import { Card, CardContent } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { date: "2023-12-01", volume: 1200000 },
  { date: "2023-12-02", volume: 1500000 },
  { date: "2023-12-03", volume: 900000 },
  { date: "2023-12-04", volume: 1700000 },
  { date: "2023-12-05", volume: 2100000 },
]

export function VolumeChart() {
  return (
    <Card>
      <CardContent className="pt-6">
        <ChartContainer
          config={{
            volume: {
              label: "Volume",
              color: "hsl(var(--muted-foreground))",
            },
          }}
          className="h-[100px]"
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <XAxis
                dataKey="date"
                stroke="hsl(var(--muted-foreground))"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="hsl(var(--muted-foreground))"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tickFormatter={(value) => `${value / 1000000}M`}
              />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Bar dataKey="volume" fill="hsl(var(--muted-foreground))" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

