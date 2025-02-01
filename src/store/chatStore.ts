import { create } from 'zustand';
import { ChatRoom, Message, User } from '../types/chat';
import { getFirestore, collection, addDoc, updateDoc, doc, query, where, getDocs } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { onSnapshot, orderBy } from 'firebase/firestore';
import { db, auth } from '@/lib/firebase';
import { defaultGroups } from '@/config/defaultGroups';


interface Report {
  id: string;
  reporterId: string;
  reportedId: string;
  reason: string;
  description: string;
  createdAt: Date;
  status: 'pending' | 'resolved';
}

interface GroupRequest {
  id: string;
  userId: string;
  groupId: string;
  status: 'pending' | 'accepted' | 'rejected';
  createdAt: Date;
}

interface ApologyRequest {
  id: string;
  fromUserId: string;
  toUserId: string;
  message: string;
  status: 'pending' | 'accepted' | 'rejected';
  createdAt: Date;
}

interface GroupData {
  name: string;
  description: string;
  isPublic: boolean;
  selectedUsers: string[];
  createdBy: string;
}

interface ChatState {
  currentRoom?: ChatRoom;
  rooms: ChatRoom[];
  messages: Message[];
  users: User[];
  pendingRequests: any[];
  reports: Report[];
  groupRequests: GroupRequest[];
  apologyRequests: ApologyRequest[];
  warningCounts: Record<string, number>;
  
  setCurrentRoom: (room: ChatRoom) => void;
  addMessage: (message: Message) => void;
  addRoom: (room: ChatRoom) => void;
  sendFriendRequest: (userId: string) => Promise<void>;
  acceptFriendRequest: (requestId: string) => Promise<void>;
  rejectFriendRequest: (requestId: string) => Promise<void>;
  createGroup: (groupData: GroupData) => Promise<void>;
  requestGroupJoin: (groupId: string) => Promise<void>;
  acceptGroupRequest: (requestId: string) => Promise<void>;
  rejectGroupRequest: (requestId: string) => Promise<void>;
  reportUser: (reportData: Omit<Report, 'id' | 'createdAt' | 'status'>) => Promise<void>;
  sendApology: (toUserId: string, message: string) => Promise<void>;
  acceptApology: (requestId: string) => Promise<void>;
  rejectApology: (requestId: string) => Promise<void>;
  initializeListeners: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  rooms: defaultGroups, // Add this line to initialize with default groups
  messages: [],
  users: [],
  pendingRequests: [],
  reports: [],
  groupRequests: [],
  apologyRequests: [],
  warningCounts: {},
  setCurrentRoom: (room) => set({ currentRoom: room }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  addRoom: (room) => set((state) => ({ rooms: [...state.rooms, room] })),
  
  sendFriendRequest: async (userId) => {
    const currentUser = auth.currentUser;
    if (!currentUser) return;

    const requestData = {
      senderId: currentUser.uid,
      receiverId: userId,
      status: 'pending',
      createdAt: new Date()
    };

    await addDoc(collection(db, 'friendRequests'), requestData);
  },

  acceptFriendRequest: async (requestId) => {
    const requestRef = doc(db, 'friendRequests', requestId);
    await updateDoc(requestRef, { status: 'accepted' });

    const request = get().pendingRequests.find(r => r.id === requestId);
    if (request) {
      const roomData = {
        type: 'private',
        participants: [request.senderId, request.receiverId],
        messages: []
      };
      await addDoc(collection(db, 'rooms'), roomData);
    }

    set(state => ({
      pendingRequests: state.pendingRequests.filter(r => r.id !== requestId)
    }));
  },

  rejectFriendRequest: async (requestId) => {
    const requestRef = doc(db, 'friendRequests', requestId);
    await updateDoc(requestRef, { status: 'rejected' });

    set(state => ({
      pendingRequests: state.pendingRequests.filter(r => r.id !== requestId)
    }));
  },

  createGroup: async (groupData) => {
    const currentUser = auth.currentUser;
    if (!currentUser) return;

    const newGroup = {
      ...groupData,
      createdBy: currentUser.uid,
      createdAt: new Date(),
      members: groupData.isPublic ? [currentUser.uid] : [...groupData.selectedUsers, currentUser.uid],
      type: 'group'
    };

    await addDoc(collection(db, 'rooms'), newGroup);
  },

  requestGroupJoin: async (groupId) => {
    const currentUser = auth.currentUser;
    if (!currentUser) return;

    const requestData = {
      userId: currentUser.uid,
      groupId,
      status: 'pending',
      createdAt: new Date()
    };

    await addDoc(collection(db, 'groupRequests'), requestData);
  },

  acceptGroupRequest: async (requestId) => {
    const request = get().groupRequests.find(r => r.id === requestId);
    if (!request) return;

    const groupRef = doc(db, 'rooms', request.groupId);
    await updateDoc(groupRef, {
      members: arrayUnion(request.userId)
    });

    await updateDoc(doc(db, 'groupRequests', requestId), {
      status: 'accepted'
    });
  },

  rejectGroupRequest: async (requestId) => {
    await updateDoc(doc(db, 'groupRequests', requestId), {
      status: 'rejected'
    });
  },

  reportUser: async (reportData) => {
    const currentUser = auth.currentUser;
    if (!currentUser) return;

    const newReport = {
      ...reportData,
      reporterId: currentUser.uid,
      createdAt: new Date(),
      status: 'pending'
    };

    await addDoc(collection(db, 'reports'), newReport);

    // Update warning count
    const warningCount = (get().warningCounts[reportData.reportedId] || 0) + 1;
    set(state => ({
      warningCounts: {
        ...state.warningCounts,
        [reportData.reportedId]: warningCount
      }
    }));

    if (warningCount >= 3) {
      // Restrict user
      await updateDoc(doc(db, 'users', reportData.reportedId), {
        status: 'restricted'
      });
    }
  },

  sendApology: async (toUserId, message) => {
    const currentUser = auth.currentUser;
    if (!currentUser) return;

    const apologyData = {
      fromUserId: currentUser.uid,
      toUserId,
      message,
      status: 'pending',
      createdAt: new Date()
    };

    await addDoc(collection(db, 'apologyRequests'), apologyData);
  },

  acceptApology: async (requestId) => {
    const request = get().apologyRequests.find(r => r.id === requestId);
    if (!request) return;

    await updateDoc(doc(db, 'apologyRequests', requestId), {
      status: 'accepted'
    });

    // Reset warning count
    set(state => ({
      warningCounts: {
        ...state.warningCounts,
        [request.fromUserId]: 0
      }
    }));

    // Remove restriction
    await updateDoc(doc(db, 'users', request.fromUserId), {
      status: 'active'
    });
  },

  rejectApology: async (requestId) => {
    await updateDoc(doc(db, 'apologyRequests', requestId), {
      status: 'rejected'
    });
  },

  initializeListeners: () => {
    const currentUser = auth.currentUser;
    if (!currentUser) return;

    // Listen for friend requests
    const requestsQuery = query(
      collection(db, 'friendRequests'),
      where('receiverId', '==', currentUser.uid),
      where('status', '==', 'pending'),
      orderBy('createdAt', 'desc')
    );

    onSnapshot(requestsQuery, (snapshot) => {
      const requests = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      set({ pendingRequests: requests });
    });

    // Listen for group requests
    const groupRequestsQuery = query(
      collection(db, 'groupRequests'),
      where('status', '==', 'pending'),
      orderBy('createdAt', 'desc')
    );

    onSnapshot(groupRequestsQuery, (snapshot) => {
      const requests = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      set({ groupRequests: requests });
    });

    // Listen for apology requests
    const apologyRequestsQuery = query(
      collection(db, 'apologyRequests'),
      where('toUserId', '==', currentUser.uid),
      where('status', '==', 'pending'),
      orderBy('createdAt', 'desc')
    );

    onSnapshot(apologyRequestsQuery, (snapshot) => {
      const requests = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      set({ apologyRequests: requests });
    });

    // Listen for users
    onSnapshot(collection(db, 'users'), (snapshot) => {
      const users = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      set({ users });
    });

    // Listen for rooms
    onSnapshot(collection(db, 'rooms'), (snapshot) => {
      const rooms = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      set({ rooms });
    });
  }
}));
