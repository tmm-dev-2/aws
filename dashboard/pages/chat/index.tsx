import { useEffect, useState } from 'react';
import { Socket } from 'socket.io-client/build/esm/socket';
import { Container, Grid, Paper } from '@mantine/core';
import ChatSidebar from 'dashboard/components/ChatSidebar';
import ChatWindow from 'dashboard/components/ChatWindow';
import { useChatStore } from 'dashboard/store/chatStore';

let socket: Socket;

export default function ChatPage() {
  const [connected, setConnected] = useState(false);
  const { addMessage } = useChatStore();

  useEffect(() => {
    socket = io('http://localhost:3001');

    socket.on('connect', () => {
      setConnected(true);
    });

    socket.on('private_message', (message) => {
      addMessage(message);
    });

    socket.on('group_message', (message) => {
      addMessage(message);
    });

    socket.on('bot_message', (message) => {
      addMessage(message);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <Container size="xl" p={0}>
      <Grid grow>
        <Grid.Col span={3}>
          <Paper shadow="xs">
            <ChatSidebar socket={socket} />
          </Paper>
        </Grid.Col>
        <Grid.Col span={9}>
          <Paper shadow="xs">
            <ChatWindow socket={socket} />
          </Paper>
        </Grid.Col>
      </Grid>
    </Container>
  );
}
