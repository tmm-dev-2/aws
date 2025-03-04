import { Server } from 'socket.io';
import { createServer } from 'http';
import { ChatRoom, Message, User } from '../types/chat';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: {
    origin: process.env.NEXT_PUBLIC_FRONTEND_URL,
    methods: ['GET', 'POST'],
  },
});

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  socket.on('private_message', async (data) => {
    const message = {
      id: Date.now().toString(),
      content: data.content,
      senderId: socket.id,
      createdAt: new Date(),
      isBot: false
    };
    
    io.to(data.roomId).emit('private_message', message);
  });

  socket.on('group_message', async (data) => {
    const message = {
      id: Date.now().toString(),
      content: data.content,
      senderId: socket.id,
      createdAt: new Date(),
      isBot: false
    };
    
    io.to(data.roomId).emit('group_message', message);
  });

  socket.on('start_bot_chat', async () => {
    const botRoom = {
      id: `bot-${socket.id}`,
      type: 'bot',
      participants: [],
      messages: []
    };
    socket.emit('bot_room_created', botRoom);
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

httpServer.listen(3001);
