"use client"

import { Card } from "@/dashboard-components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/dashboard-components/ui/tabs"

export default function MarketSummary() {
  return (
    <Card>
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="details">Details</TabsTrigger>
        </TabsList>
        <TabsContent value="overview">
          <p>Overview content here</p>
        </TabsContent>
        <TabsContent value="details">
          <p>Details content here</p>
        </TabsContent>
      </Tabs>
    </Card>
  )
}

