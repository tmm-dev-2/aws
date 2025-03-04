import React, { useState } from 'react';
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Plus } from 'lucide-react';
import { useChatStore } from 'dashboard/store/chatStore';

interface CreateGroupModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CreateGroupModal({ isOpen, onClose }: CreateGroupModalProps) {
  const [groupName, setGroupName] = useState('');
  const [description, setDescription] = useState('');
  const [isPublic, setIsPublic] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const { users, createGroup, addRoom } = useChatStore();

  const filteredUsers = users.filter(user => 
    user.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCreateGroup = async () => {
    if (!groupName.trim()) return;

    const newGroup = {
      id: Date.now().toString(),
      name: groupName,
      description,
      type: 'group',
      isPublic,
      participants: [],
      messages: []
    };

    await createGroup(newGroup);
    addRoom(newGroup);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-[#1a1a1a] p-6 rounded-lg w-96">
        <h2 className="text-xl mb-4 text-white">Create New Group</h2>
        
        <Input
          placeholder="Group Name"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          className="mb-4"
        />
        
        <Input
          placeholder="Group Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="mb-4"
        />
        
        <div className="flex items-center mb-4">
          <input
            type="checkbox"
            checked={isPublic}
            onChange={(e) => setIsPublic(e.target.checked)}
            className="mr-2"
          />
          <span className="text-white">Public Group</span>
        </div>
        
        <div className="mb-4">
          <Input
            placeholder="Search users..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="mb-2"
          />
          <div className="max-h-60 overflow-y-auto">
            {filteredUsers.map(user => (
              <div key={user.id} className="flex items-center justify-between p-2 hover:bg-[#2a2a2a] rounded">
                <span className="text-white">{user.name}</span>
                <Button
                  size="sm"
                  variant="ghost"
                  className="hover:bg-[#3a3a3a]"
                  title="Add to Group"
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>
        
        <div className="flex justify-end space-x-2">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleCreateGroup}>
            Create Group
          </Button>
        </div>
      </div>
    </div>
  );
}
