import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useDocument } from 'react-firebase-hooks/firestore';
import { doc } from 'firebase/firestore';
import { db } from '../config/firebase';

export default function ProfilePage() {
    const { user } = useAuth();
    const [userData, loading] = useDocument(
        user ? doc(db, 'users', user.uid) : null
    );

    if (loading) return <div>Loading...</div>;
    if (!user || !userData?.exists()) return <div>Not found</div>;

    const data = userData.data();

    return (
        <div className="min-h-screen bg-[#1a1a1a] p-6">
            <div className="max-w-4xl mx-auto">
                <div className="bg-[#242424] rounded-lg p-6">
                    <div className="flex items-center gap-6">
                        <img 
                            src={user.photoURL || '/default-avatar.png'} 
                            alt="Profile" 
                            className="w-24 h-24 rounded-full"
                        />
                        <div>
                            <h1 className="text-2xl font-bold text-white">{user.displayName}</h1>
                            <p className="text-gray-400">{user.email}</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-4 gap-4 mt-8 text-center">
                        <div className="bg-[#1a1a1a] p-4 rounded">
                            <div className="text-2xl font-bold text-white">{data.followers?.length || 0}</div>
                            <div className="text-gray-400">Followers</div>
                        </div>
                        <div className="bg-[#1a1a1a] p-4 rounded">
                            <div className="text-2xl font-bold text-white">{data.following?.length || 0}</div>
                            <div className="text-gray-400">Following</div>
                        </div>
                        <div className="bg-[#1a1a1a] p-4 rounded">
                            <div className="text-2xl font-bold text-white">{data.publishedBots?.length || 0}</div>
                            <div className="text-gray-400">Bots</div>
                        </div>
                        <div className="bg-[#1a1a1a] p-4 rounded">
                            <div className="text-2xl font-bold text-white">{data.publishedIdeas?.length || 0}</div>
                            <div className="text-gray-400">Ideas</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
