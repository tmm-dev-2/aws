import { Message } from '@/types/chat';
import { format } from 'date-fns';
import { FileIcon, ImageIcon, Smile } from 'lucide-react';
import EmojiPicker from 'emoji-picker-react';

interface MessageListProps {
  messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
  return (
    <div className="flex flex-col space-y-6 px-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.senderId === 'currentUser' ? 'justify-end' : 'justify-start'} group`}
        >
          {message.senderId !== 'currentUser' && (
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-400 to-pink-500 flex-shrink-0 mr-2">
              <img 
                src={message.senderAvatar || '/default-avatar.png'} 
                className="w-full h-full rounded-full object-cover"
                alt={message.senderId}
              />
            </div>
          )}
          
          <div className="flex flex-col max-w-[70%]">
            {message.senderId !== 'currentUser' && (
              <span className="text-xs text-gray-400 ml-2 mb-1">{message.senderId}</span>
            )}
            
            <div
              className={`rounded-2xl p-3 ${
                message.senderId === 'currentUser'
                  ? 'bg-blue-500 rounded-br-none'
                  : 'bg-[#2a2a2a] rounded-bl-none'
              }`}
            >
              {message.fileUrl && message.fileType === 'image' ? (
                <img 
                  src={message.fileUrl} 
                  className="rounded-lg max-w-full mb-2" 
                  alt="Shared image"
                />
              ) : message.fileUrl ? (
                <div className="flex items-center space-x-2 mb-2 bg-[#1a1a1a] p-2 rounded">
                  <FileIcon className="h-4 w-4" />
                  <a href={message.fileUrl} className="text-blue-400 hover:underline text-sm">
                    {message.fileName}
                  </a>
                </div>
              ) : null}
              
              <p className="text-white whitespace-pre-wrap break-words">{message.content}</p>
              
              <div className="flex justify-between items-center mt-1">
                <span className="text-xs text-gray-300">
                  {format(new Date(message.createdAt), 'HH:mm')}
                </span>
                {message.senderId === 'currentUser' && (
                  <span className="text-xs text-gray-300">
                    {message.status === 'sent' ? '✓' : '✓✓'}
                  </span>
                )}
              </div>
            </div>
            
            <div className="opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="flex space-x-2 mt-1">
                <button className="text-gray-400 hover:text-white">
                  <Smile className="h-4 w-4" />
                </button>
                <button className="text-gray-400 hover:text-white">
                  Reply
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
