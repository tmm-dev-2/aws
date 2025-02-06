"use client"

import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const ideas = [
  {
    title: "KSB Ltd: Channel Breakout on Budget 2025 Irrigation Boost",
    description: "Details: Asset: KSB Ltd Breakout Level: Channel breakout confirmed",
    author: "CyborgTradingHub",
    date: "Feb 1",
    comments: 1,
    likes: 17,
  },
  {
    title: "Inverse head-and-shoulders - Coal India",
    description:
      "Inverse head-and-shoulders chart pattern is an important indicator for identifying bullish reversals.",
    author: "Bharatk4u",
    date: "Jan 30",
    comments: 3,
    likes: 142,
  },
  {
    title: "MAZDOCK - Ready for the next move",
    description: "The stock has been a market favorite. Technically it has cooled down owing to the Wave analysis.",
    author: "CannySunny",
    date: "Jan 30",
    comments: 3,
    likes: 125,
  },
]

export function CommunityIdeas() {
  return (
    <Tabs defaultValue="editors-picks" className="mt-4">
      <TabsList>
        <TabsTrigger value="editors-picks">Editors&apos; picks</TabsTrigger>
        <TabsTrigger value="for-you">For you</TabsTrigger>
        <TabsTrigger value="following">Following</TabsTrigger>
        <TabsTrigger value="popular">Popular</TabsTrigger>
      </TabsList>
      <TabsContent value="editors-picks" className="mt-4">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {ideas.map((idea) => (
            <Card key={idea.title} className="overflow-hidden">
              <div className="aspect-[4/3] bg-muted/20">
                {/* Placeholder for chart */}
                <div className="flex h-full items-center justify-center">
                  <p className="text-muted-foreground">Chart placeholder</p>
                </div>
              </div>
              <CardHeader className="p-4">
                <h3 className="line-clamp-2 text-base font-semibold">{idea.title}</h3>
                <p className="line-clamp-2 text-sm text-muted-foreground">{idea.description}</p>
              </CardHeader>
              <CardContent className="flex items-center justify-between p-4 pt-0">
                <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                  <span>{idea.author}</span>
                  <span>•</span>
                  <span>{idea.date}</span>
                </div>
                <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                  <span>{idea.comments} 💬</span>
                  <span>{idea.likes} 👍</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </TabsContent>
    </Tabs>
  )
}

