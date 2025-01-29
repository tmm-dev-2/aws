import { List } from '@mantine/core';
import { Text } from '@mantine/core';
import { useChatStore } from '@/store/chatStore';
import { Group } from '@/types/chat';

interface GroupListProps {
  groups: Group[];
  showGroupInfo: (group: Group) => void;
}

export default function GroupList({ groups, showGroupInfo }: GroupListProps) {
  const { setCurrentRoom } = useChatStore();

  return (
    <List spacing="xs">
      {groups.map((group) => (
        <List.Item 
          key={group.id}
          onClick={() => setCurrentRoom(group)}
          style={{ cursor: 'pointer' }}
        >
          <div className="flex items-center justify-between p-3">
            <Text>{group.name}</Text>
            <Text size="sm" color="dimmed">
              {group.members.length} members
            </Text>
          </div>
        </List.Item>
      ))}
    </List>
  );
}
