import { Group } from 'dashboard/types/chat';
import { List, Text } from '@mantine/core';
import { useChatStore } from 'dashboard/store/chatStore';

interface UserListProps {
  users: User[];
}

export default function UserList({ users }: UserListProps) {
  const { setCurrentRoom } = useChatStore();

  const startChat = (user: User) => {
    setCurrentRoom({
      id: `private-${user.id}`,
      type: 'private',
      participants: [user],
      messages: []
    });
  };

  return (
    <List spacing="xs">
      {users.map((user) => (
        <List.Item 
          key={user.id}
          onClick={() => startChat(user)}
          style={{ cursor: 'pointer' }}
        >
          <Text>{user.name}</Text>
        </List.Item>
      ))}
    </List>
  );
}
