'use client';

import { MantineProvider } from '@mantine/core';
import React, { useRef, useState, useEffect } from 'react';
import { Search, UserPlus, Users, Settings, Plus, Paperclip, Smile , Info} from 'lucide-react';
import { Button } from "../components/ui/button";
import { Input as TextInput } from "../components/ui/input";
import { Tabs, TabsList, TabsTab, TabsPanel } from "../components/Tabs";
import MessageList from '@/components/MessageList';
import UserList from '@/components/UserList';
import GroupList from '@/components/GroupList';
import { useChatStore } from '@/store/chatStore';
import socketIOClient from 'socket.io-client';
import '../app/globals.css';
import EmojiPicker from 'emoji-picker-react';
import { CreateGroupModal } from '@/components/CreateGroupModal';
import { MessageActions } from '@/components/MessageActions';
import { WarningBanner } from '@/components/WarningBanner';

const defaultGroups = [
  { 
    id: '1', 
    name: 'Forex',
    type: 'group',
    participants: [],
    messages: [],
    description: 'Discuss forex trading strategies and market analysis',
    isPublic: true,
    members: []
  },
  { 
    id: '2', 
    name: 'India',
    type: 'group',
    participants: [],
    messages: [],
    description: 'Indian market discussion and analysis',
    isPublic: true,
    members: []
  },
  { 
    id: '3', 
    name: 'USA',
    type: 'group',
    participants: [],
    messages: [],
    description: 'US market trends and trading opportunities',
    isPublic: true,
    members: []
  },
  { 
    id: '4', 
    name: 'Crypto',
    type: 'group',
    participants: [],
    messages: [],
    description: 'Cryptocurrency trading and blockchain technology',
    isPublic: true,
    members: []
  },
  { 
    id: '5', 
    name: 'AI Assistant',
    type: 'ai',
    participants: [],
    messages: [],
    description: 'Chat with multiple AI models for analysis and insights',
    isPublic: true,
    members: [],
    isAiChat: true
  }
];

const MODELS = [
  { id: 'mxbai-embed-large', name: 'MXBAI Embed Large', description: 'Best for embeddings and semantic search' },
  { id: 'minicpm-v', name: 'MiniCPM-V', description: 'Efficient multilingual model' },
  { id: 'qwen2.5-coder', name: 'Qwen 2.5 Coder', description: 'Specialized for code generation' },
  { id: 'codegemma', name: 'CodeGemma', description: 'Advanced code understanding' },
  { id: 'codellama', name: 'CodeLlama', description: 'Meta\'s code generation model' },
  { id: 'llama3.2-vision', name: 'Llama 3.2 Vision', description: 'Multimodal capabilities' }
];

function ChatContent() {
  const { messages, rooms, users, pendingRequests, initializeListeners, addMessage, warningCounts } = useChatStore();
  const [activeTab, setActiveTab] = useState('messages');
  console.log("Default Groups:", defaultGroups);
  console.log("Store Rooms:", rooms);
  const [showAddContact, setShowAddContact] = useState(false);
  const [showCreateGroup, setShowCreateGroup] = useState(false);
  const [showGroupInfo, setShowGroupInfo] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const messageRef = useRef<HTMLInputElement>(null);
  const socket = socketIOClient('http://localhost:3001', {
    transports: ['websocket'],
    autoConnect: true
  });

  useEffect(() => {
    initializeListeners();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const newMessage = {
        id: Date.now().toString(),
        content: '',
        senderId: 'currentUser',
        createdAt: new Date(),
        isBot: false,
        fileUrl: event.target?.result as string,
        fileName: file.name,
        fileType: file.type.startsWith('image/') ? 'image' : 'file'
      };
      
      socket.emit('message', newMessage);
      addMessage(newMessage);
    };
    reader.readAsDataURL(file);
  };

  const sendMessage = () => {
    if (messageRef.current?.value) {
      const newMessage = {
        id: Date.now().toString(),
        content: messageRef.current.value,
        senderId: 'currentUser',
        createdAt: new Date(),
        isBot: false
      };
      
      socket.emit('message', newMessage);
      addMessage(newMessage);
      messageRef.current.value = '';
    }
  };

  const handleGroupClick = (group) => {
    if (group.isPublic) {
      // Join directly
      socket.emit('join_group', group.id);
    } else {
      // Send join request
      socket.emit('request_join_group', group.id);
    }
  };

  const showGroupDetails = (group) => {
    setSelectedGroup(group);
    setShowGroupInfo(true);
  };

  return (
    <div className="flex h-screen bg-[#1a1a1a] text-white">
      {/* Icon Sidebar */}
      <div className="w-16 bg-[#151515] border-r border-[#2a2a2a] flex flex-col items-center py-4">
        <div className="space-y-6">
          <Button
            variant="ghost"
            size="icon"
            className="hover:bg-[#2a2a2a]"
            title="Add Contact"
            onClick={() => setShowAddContact(true)}
          >
            <UserPlus className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="hover:bg-[#2a2a2a]"
            title="Create Group"
            onClick={() => setShowCreateGroup(true)}
          >
            <Users className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="hover:bg-[#2a2a2a]"
            title="Settings"
          >
            <Settings className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Main Sidebar */}
      <div className="w-80 border-r border-[#2a2a2a] flex flex-col">
        <div className="p-4 border-b border-[#2a2a2a]">
          <div className="relative">
            <TextInput
              placeholder="Search..."
              className="mb-2 pl-8 bg-[#2a2a2a] text-white"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <Search className="h-4 w-4 absolute left-2 top-3 text-gray-400" />
          </div>
        </div>

        {warningCounts['currentUser'] > 0 && (
          <WarningBanner warningCount={warningCounts['currentUser']} />
        )}

        <div className="flex-1 flex flex-col">
          <div className="h-3/5 overflow-y-auto custom-scrollbar">
            <Tabs defaultValue="messages" onValueChange={setActiveTab}>
            <TabsList className="sticky top-0 bg-[#1a1a1a] border-b border-[#2a2a2a] px-4">
              <TabsTab value="messages" onValueChange={setActiveTab}>Messages</TabsTab>
              <TabsTab value="contacts" onValueChange={setActiveTab}>Contacts</TabsTab>
              <TabsTab value="groups" onValueChange={setActiveTab}>Groups</TabsTab>
            </TabsList>


              <div className="p-4">
                <TabsPanel value="messages">
                  <MessageList messages={messages} />
                </TabsPanel>

                <TabsPanel value="contacts">
                  <UserList users={users} />
                </TabsPanel>

                <TabsPanel value="groups">
                  {(() => {
                    console.log('Default Groups:', defaultGroups)
                    console.log('Rooms:', rooms)
                    return (
                      <div className="space-y-2">
                        {defaultGroups.map(group => (
                          <div 
                            key={group.id} 
                            className="flex items-center justify-between p-3 bg-[#2a2a2a] rounded-lg hover:bg-[#3a3a3a] cursor-pointer"
                          >
                            <div className="flex items-center space-x-3">
                              <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white">
                                {group.name[0]}
                              </div>
                              <div>
                                <p className="font-medium text-white">{group.name}</p>
                                <p className="text-sm text-gray-400">{group.description}</p>
                              </div>
                            </div>
                            <Info className="h-4 w-4 text-gray-400" />
                          </div>
                        ))}
                      </div>
                    )
                  })()}
                </TabsPanel>


              </div>
            </Tabs>
          </div>

          <div className="h-2/5 border-t border-[#2a2a2a]">
            <div className="p-4">
              <h3 className="text-sm font-semibold mb-4">
                Pending Requests ({pendingRequests.length})
              </h3>
              <div className="space-y-3">
                {pendingRequests.map(request => (
                  <div key={request.id} className="p-3 bg-[#2a2a2a] rounded-lg">
                    {request.type === 'friend' && (
                      <div>Friend request from {request.senderName}</div>
                    )}
                    {request.type === 'group' && (
                      <div>Group join request for {request.groupName}</div>
                    )}
                    {request.type === 'apology' && (
                      <div>Apology request from {request.senderName}</div>
                    )}
                    <div className="flex space-x-2 mt-2">
                      <Button size="sm" onClick={() => acceptRequest(request.id)}>
                        Accept
                      </Button>
                      <Button size="sm" variant="ghost" onClick={() => rejectRequest(request.id)}>
                        Reject
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {showAddContact && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-[#1a1a1a] p-6 rounded-lg w-96">
            <h2 className="text-xl mb-4">Add Contact</h2>
            <TextInput
              placeholder="Search users..."
              className="mb-4"
            />
            <div className="max-h-60 overflow-y-auto">
              {users.map(user => (
                <div key={user.id} className="flex items-center justify-between p-2 hover:bg-[#2a2a2a] rounded">
                  <span>{user.name}</span>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="hover:bg-[#3a3a3a]"
                    title="Send Request"
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
            <Button
              className="mt-4"
              onClick={() => setShowAddContact(false)}
            >
              Close
            </Button>
          </div>
        </div>
      )}

      {showCreateGroup && (
        <CreateGroupModal
          isOpen={showCreateGroup}
          onClose={() => setShowCreateGroup(false)}
        />
      )}

      {showGroupInfo && selectedGroup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-[#1a1a1a] p-6 rounded-lg w-96">
            <h2 className="text-xl mb-4">{selectedGroup.name}</h2>
            <p className="text-gray-400 mb-4">{selectedGroup.description}</p>
            <div className="mb-4">
              <p className="text-sm text-gray-400">Members: {selectedGroup.members.length}</p>
              <p className="text-sm text-gray-400">Type: {selectedGroup.isPublic ? 'Public' : 'Private'}</p>
            </div>
            <Button
              className="w-full"
              onClick={() => setShowGroupInfo(false)}
            >
              Close
            </Button>
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-4">
          <MessageList messages={messages} />
        </div>

        <div className="p-4 border-t border-[#2a2a2a]">
          <div className="flex items-center gap-2">
            <button 
              className="p-2 hover:bg-[#2a2a2a] rounded-full"
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
            >
              <Smile className="h-5 w-5 text-gray-400" />
            </button>
            
            <label className="p-2 hover:bg-[#2a2a2a] rounded-full cursor-pointer">
              <input 
                type="file" 
                className="hidden" 
                onChange={handleFileUpload}
                accept="image/*,.pdf,.doc,.docx"
              />
              <Paperclip className="h-5 w-5 text-gray-400" />
            </label>
            
            <input
              ref={messageRef}
              type="text"
              placeholder="Type a message..."
              className="flex-1 min-w-0 bg-[#2a2a2a] text-white px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            />
            <Button 
              size="sm" 
              onClick={sendMessage}
              className="bg-blue-500 hover:bg-blue-600 text-white px-6"
            >
              Send
            </Button>
          </div>
          
          {showEmojiPicker && (
            <div className="absolute bottom-20 right-4">
              <EmojiPicker
                onEmojiClick={(emoji) => {
                  if (messageRef.current) {
                    messageRef.current.value += emoji.emoji;
                  }
                }}
                theme="dark"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Chat() {
  return (
    <MantineProvider>
      <ChatContent />
    </MantineProvider>
  );
}