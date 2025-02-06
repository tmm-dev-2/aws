"use client"

import { Card, CardContent, CardHeader } from "@/dashboard-components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/dashboard-components/ui/tabs"

export default function CommunityIdeas() {
  return (
    <Card>
      <CardHeader>Community Ideas</CardHeader>
      <CardContent>
        <Tabs defaultValue="ideas">
          <TabsList>
            <TabsTrigger value="ideas">Ideas</TabsTrigger>
            <TabsTrigger value="discussions">Discussions</TabsTrigger>
          </TabsList>
          <TabsContent value="ideas">
            <p>List of community ideas here.</p>
          </TabsContent>
          <TabsContent value="discussions">
            <p>List of community discussions here.</p>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}

