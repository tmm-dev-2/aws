import React from 'react';
import Image from 'next/image';

export function IdeaCard({ idea }: { idea: TradingIdea }) {
  return (
    <div className="bg-[#242424] rounded-lg p-4">
      <div className="flex items-center gap-3 mb-4">
        <Image
          src={idea.author.avatar}
          alt={idea.author.name}
          width={40}
          height={40}
          className="rounded-full"
        />
        <div>
          <h3 className="font-semibold text-white">{idea.author.name}</h3>
          <p className="text-sm text-gray-400">
            {new Date(idea.createdAt).toLocaleDateString()}
          </p>
        </div>
      </div>
      
      <h2 className="text-xl font-bold text-white mb-2">{idea.title}</h2>
      <div className="mb-4">
        <Image
          src={idea.chartImage}
          alt="Trading Chart"
          width={800}
          height={400}
          className="rounded-lg"
        />
      </div>
      <p className="text-gray-200 mb-4">{idea.description}</p>
      
      <div className="flex items-center gap-4">
        <ReactionBar idea={idea} />
        <CommentSection idea={idea} />
      </div>
    </div>
  );
}
