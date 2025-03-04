import { useRef } from 'react';
import { Paper, TextInput, Button } from '@mantine/core';
import { Socket } from 'socket.io-client/build/esm/socket';
import { useChatStore } from 'dashboard/store/chatStore';
import MessageList from './MessageList';

interface ChatWindowProps {
  socket: Socket;
}

export default function ChatWindow({ socket }: ChatWindowProps) {
  const messageRef = useRef<HTMLInputElement>(null);
  const { currentRoom, messages } = useChatStore();

  const sendMessage = () => {
    if (!messageRef.current?.value) return;

    const messageData = {
      content: messageRef.current.value,
      roomId: currentRoom?.id,
      type: currentRoom?.type,
    };

    socket.emit('${currentRoom?.type}_message', messageData);
    messageRef.current.value = '';
  };

  return (
    <div className="bg-[#202123] flex flex-col h-full">
      <Paper className="h-[70vh] overflow-y-auto bg-[#202123] text-white">
        <MessageList messages={messages} />
      </Paper>
      
      <div className="flex flex-row items-center mt-2">
        <TextInput
          ref={messageRef}
          placeholder="Type your message..."
          className="flex-1 bg-[#343536] text-white"
        />
        <Button onClick={sendMessage} className="ml-2 bg-[#007BFF] text-white hover:bg-[#0056b3]">Send</Button>
      </div>
    </div>
  );
}
