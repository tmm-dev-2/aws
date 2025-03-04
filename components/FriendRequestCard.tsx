import { User } from 'dashboard/types/chat';
import { Check, X } from 'lucide-react';
import { Button } from './ui/button';
import { useChatStore } from 'dashboard/store/chatStore';

interface FriendRequestCardProps {
  request: {
    id: string;
    sender: User;
  };
}

export function FriendRequestCard({ request }: FriendRequestCardProps) {
  const { acceptFriendRequest, rejectFriendRequest } = useChatStore();

  return (
    <div className="flex items-center justify-between p-3 bg-[#2a2a2a] rounded-lg">
      <div className="flex items-center space-x-3">
        <img 
          src={request.sender.image || '/default-avatar.png'} 
          className="w-10 h-10 rounded-full"
          alt={request.sender.name}
        />
        <div>
          <p className="font-medium">{request.sender.name}</p>
          <p className="text-sm text-gray-400">{request.sender.email}</p>
        </div>
      </div>
      <div className="flex space-x-2">
        <Button
          size="sm"
          variant="ghost"
          className="text-green-500 hover:text-green-400 hover:bg-green-500/10"
          onClick={() => acceptFriendRequest(request.id)}
        >
          <Check className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          className="text-red-500 hover:text-red-400 hover:bg-red-500/10"
          onClick={() => rejectFriendRequest(request.id)}
        >
          <X className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
