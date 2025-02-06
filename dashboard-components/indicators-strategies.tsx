"use client"

import { Card, CardContent, CardHeader } from "@/dashboard-components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/dashboard-components/ui/tabs"

export default function IndicatorsStrategies() {
  return (
    <Card>
      <CardHeader>Indicators & Strategies</CardHeader>
      <CardContent>
        <Tabs defaultValue="overview">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="indicators">Indicators</TabsTrigger>
            <TabsTrigger value="strategies">Strategies</TabsTrigger>
          </TabsList>
          <TabsContent value="overview">
            <p>Overview content here</p>
          </TabsContent>
          <TabsContent value="indicators">
            <p>Indicators content here</p>
          </TabsContent>
          <TabsContent value="strategies">
            <p>Strategies content here</p>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}

