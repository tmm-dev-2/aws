export interface User {
  id: string;
  name: string;
  email: string;
  image?: string;
}

export interface Message {
  id: string;
  content: string;
  senderId: string;
  receiverId?: string;
  groupId?: string;
  createdAt: Date;
  isBot: boolean;
}

export interface Group {
  id: string;
  name: string;
  description?: string;
  members: User[];
  admins: User[];
}

export interface ChatRoom {
  id: string;
  type: 'private' | 'group' | 'bot';
  participants: User[];
  messages: Message[];
  lastMessage?: Message;
  name: string;
  description?: string;
  isPublic: boolean;
  members: User[];
}
