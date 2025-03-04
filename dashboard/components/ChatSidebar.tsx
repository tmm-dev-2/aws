import { useState } from 'react';
import { Stack, TextInput, Button, Box } from '@mantine/core';
import { Socket } from 'socket.io-client/build/esm/socket';
import { useChatStore } from 'dashboard/store/chatStore';
import UserList from './UserList';
import GroupList from './GroupList';
import FriendRequestList from './FriendRequestList';

interface ChatSidebarProps {
  socket: Socket;
}

export default function ChatSidebar({ socket }: ChatSidebarProps) {
  const { users, rooms } = useChatStore();

  const startBotChat = () => {
    socket.emit('start_bot_chat');
  };

  return (
    <div className="bg-[#202123] text-white flex h-full">
          {/* Icon Bar */}
          <div className="w-16 flex flex-col items-center p-2">
            <div className="text-xl font-bold mb-4">
              <span>Logo</span> {/* Placeholder logo */}
            </div>
            <div className="mb-4 space-y-4">
              {/* Placeholder Icons - Replace with actual icons */}
              <div className="p-2 hover:bg-[#343536] rounded-md cursor-pointer">Chats Icon</div>
              <div className="p-2 hover:bg-[#343536] rounded-md cursor-pointer">Contacts Icon</div>
              <div className="p-2 hover:bg-[#343536] rounded-md cursor-pointer">Groups Icon</div>
              <div className="p-2 hover:bg-[#343536] rounded-md cursor-pointer">Settings Icon</div>
            </div>
          </div>
    
          {/* Content Area */}
          <div className="flex-1 p-4 flex flex-col">
            <div className="text-xl font-bold mb-4">Chats</div>
            <TextInput placeholder="Search chats..." className="mb-4 bg-[#343536] text-white" />
            <div className="p-2 rounded hover:bg-[#343536] cursor-pointer">
              <div className="font-bold flex items-center">
                <span>Archived</span>
              </div>
            </div>
            <div className="p-2 rounded hover:bg-[#343536] cursor-pointer">
              <div className="font-bold flex items-center">
                <span>Pinned</span>
              </div>
            </div>
            <div className="p-2 rounded hover:bg-[#343536] cursor-pointer">
              <div className="font-bold flex items-center">
                <span>All Chats</span>
              </div>
            </div>
            <UserList users={users} />
            <GroupList
              groups={rooms
                .filter(r => r.type === 'group')
                .map(room => ({
                  id: room.id,
                  name: room.id, // Using room.id as name for now
                  members: room.participants,
                  admins: [], // Defaulting to empty admins array
                }))}
            />
            <FriendRequestList />
    
            <Button onClick={startBotChat} className="mt-4 bg-[#007BFF] text-white hover:bg-[#0056b3]">Chat with AI Bot</Button>
          </div>
        </div>
  );
}
