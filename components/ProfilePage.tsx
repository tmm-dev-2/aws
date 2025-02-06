import React, { useState, useEffect } from 'react';
import { auth, db } from '../config/firebase';
import { doc, getDoc, updateDoc, collection, query, where, getDocs } from 'firebase/firestore';
import { signOut } from 'firebase/auth';
import { motion } from 'framer-motion';
import { createAvatar } from '@dicebear/core';
import { avataaars } from '@dicebear/collection';
import Image from 'next/image';

const AVATAR_STYLES = Array(50).fill(null).map((_, i) => ({
    seed: `avatar-${i}`,
    colors: [
        ["#000000", "#FFFFFF", "#666666"],
        ["#1A1A1A", "#2A2A2A", "#3A3A3A"],
        ["#FFFFFF", "#F0F0F0", "#E0E0E0"],
        ["#2B2D42", "#8D99AE", "#EDF2F4"],
        ["#2B2D42", "#8D99AE", "#EDF2F4"]
    ][i % 5],
    background: [
        'bg-gradient-to-r from-gray-900 to-black',
        'bg-gradient-to-r from-[#1A1A1A] to-[#2A2A2A]',
        'bg-gradient-to-b from-black to-[#1A1A1A]',
        'bg-gradient-to-r from-[#2B2D42] to-[#8D99AE]',
        'bg-gradient-to-b from-[#2B2D42] to-[#EDF2F4]'
    ][i % 5],
    options: {
        hair: ['long', 'short', 'mohawk', 'dreads'][i % 4],
        accessories: ['round', 'wayfarers', 'tiny'][i % 3],
        facialHair: ['medium', 'light', 'majestic'][i % 3],
        clothingType: ['blazer', 'sweater', 'hoodie'][i % 3],
    }
}));

interface UserData {
    avatarSeed?: string;
    avatarColors?: string[];
    avatarOptions?: any;
    followers?: any[];
    following?: any[];
    publishedIdeas?: any[];
    publishedScripts?: any[];
}

interface IdeaData {
    id: string;
    title: string;
    description: string;
    chartImage: string;
    createdAt: any;
    author: {
        id: string;
        name: string;
        avatar: string;
    };
}

export default function ProfilePage() {
    const [userData, setUserData] = useState<UserData | null>(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('ideas');
    const [showAvatarSelect, setShowAvatarSelect] = useState(false);
    const [selectedContainer, setSelectedContainer] = useState(0);
    const [currentAvatarUrl, setCurrentAvatarUrl] = useState('');
    const [avatarUrls, setAvatarUrls] = useState<string[]>([]);
    const [userIdeas, setUserIdeas] = useState<IdeaData[]>([]);

    useEffect(() => {
        async function fetchUserData() {
            const currentUser = auth.currentUser;
            if (currentUser) {
                const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
                if (userDoc.exists()) {
                    const userData = userDoc.data() as UserData;
                    setUserData(userData);
                    generateAndSetAvatar(userData);
                }
                setLoading(false);
            }
        }
        fetchUserData();
    }, []);

    useEffect(() => {
        async function fetchUserIdeas() {
            const currentUser = auth.currentUser;
            if (!currentUser) return;
            
            try {
                const ideasRef = collection(db, 'ideas');
                // Simple query first to verify data access
                const q = query(ideasRef);
                const snapshot = await getDocs(q);
                const ideas = snapshot.docs.map(doc => ({
                    id: doc.id,
                    ...doc.data()
                })) as IdeaData[];
                // Filter client-side for now to debug
                const userIdeas = ideas.filter(idea => idea.author?.id === currentUser.uid);
                setUserIdeas(userIdeas);
                console.log('Fetched ideas:', userIdeas); // Debug log
            } catch (error) {
                console.error('Error details:', error);
            }
        }
        
        fetchUserIdeas();
    }, []);
    

    useEffect(() => {
        async function generateAvatarUrls() {
            const urls = await Promise.all(
                AVATAR_STYLES.map(async (style) => {
                    const avatar = createAvatar(avataaars, {
                        seed: style.seed,
                        backgroundColor: style.colors[0],
                        ...style.options
                    });
                    return await avatar.toDataUri();
                })
            );
            setAvatarUrls(urls);
        }
        generateAvatarUrls();
    }, []);

    async function generateAndSetAvatar(userData: UserData) {
        const avatar = createAvatar(avataaars, {
            seed: userData?.avatarSeed || AVATAR_STYLES[0].seed,
            backgroundColor: userData?.avatarColors?.[0] || AVATAR_STYLES[0].colors[0],
            ...userData?.avatarOptions || AVATAR_STYLES[0].options
        });
        const url = await avatar.toDataUri();
        setCurrentAvatarUrl(url);
    }

    const handleLogout = async () => {
        try {
            await signOut(auth);
            window.location.href = '/';
        } catch (error) {
            console.error('Logout error:', error);
        }
    };

    const handleAvatarChange = async (av: typeof AVATAR_STYLES[0]) => {
        const currentUser = auth.currentUser;
        if (currentUser) {
            try {
                await updateDoc(doc(db, 'users', currentUser.uid), {
                    avatarSeed: av.seed,
                    avatarColors: av.colors,
                    avatarOptions: av.options
                });
                
                const newUserData = {
                    ...userData,
                    avatarSeed: av.seed,
                    avatarColors: av.colors,
                    avatarOptions: av.options
                };
                
                setUserData(newUserData);
                generateAndSetAvatar(newUserData);
                setSelectedContainer(AVATAR_STYLES.findIndex(style => style.seed === av.seed));
                setShowAvatarSelect(false);
            } catch (error) {
                console.error('Avatar update error:', error);
            }
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-black">
                <div className="animate-pulse">
                    <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                </div>
            </div>
        );
    }

    const user = auth.currentUser;

    return (
        <div className="min-h-screen bg-[#1E1E1E] p-4">
            <motion.div className="max-w-7xl mx-auto rounded-xl overflow-hidden">
                <div className="bg-[#2A2A2A] p-4">
                    <div className="max-w-6xl mx-auto px-4 py-6">
                        <motion.div 
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            className="flex items-start gap-8"
                        >
                            <div className="relative group">
                                {currentAvatarUrl && (
                                    <Image
                                        src={currentAvatarUrl}
                                        alt="User Avatar"
                                        width={128}
                                        height={128}
                                        className="rounded-full cursor-pointer"
                                        onClick={() => setShowAvatarSelect(true)}
                                    />
                                )}
                                
                                {showAvatarSelect && (
                                    <motion.div 
                                        initial={{ opacity: 0, scale: 0.95 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center"
                                    >
                                        <div className="bg-[#2A2A2A] p-6 rounded-xl w-[800px] max-h-[80vh] overflow-y-auto">
                                            <div className="flex justify-between items-center mb-4">
                                                <h3 className="text-xl text-white font-bold">Select Avatar</h3>
                                                <button 
                                                    onClick={() => setShowAvatarSelect(false)}
                                                    className="text-gray-400 hover:text-white"
                                                >
                                                    ✕
                                                </button>
                                            </div>
                                            <div className="grid grid-cols-5 gap-4">
                                                {avatarUrls.map((url, index) => (
                                                    <motion.div
                                                        key={index}
                                                        whileHover={{ scale: 1.05 }}
                                                        className="cursor-pointer p-2 rounded-lg hover:bg-[#333333]"
                                                        onClick={() => handleAvatarChange(AVATAR_STYLES[index])}
                                                    >
                                                        <Image
                                                            src={url}
                                                            alt={`Avatar ${index + 1}`}
                                                            width={100}
                                                            height={100}
                                                            className="w-full h-auto"
                                                        />
                                                    </motion.div>
                                                ))}
                                            </div>
                                        </div>
                                    </motion.div>
                                )}
                            </div>

                            <div className="flex-1">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <motion.h1 
                                            initial={{ x: -20, opacity: 0 }}
                                            animate={{ x: 0, opacity: 1 }}
                                            className="text-4xl font-bold text-white mb-2"
                                        >
                                            {user?.displayName || 'Trader'}
                                        </motion.h1>
                                        <motion.p 
                                            initial={{ x: -20, opacity: 0 }}
                                            animate={{ x: 0, opacity: 1 }}
                                            transition={{ delay: 0.1 }}
                                            className="text-gray-400"
                                        >
                                            {user?.email}
                                        </motion.p>
                                    </div>
                                    <motion.button
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={handleLogout}
                                        className="px-6 py-2 bg-white/10 hover:bg-white/20 text-white rounded-full backdrop-blur-sm transition-all"
                                    >
                                        Logout
                                    </motion.button>
                                </div>

                                <motion.div 
                                    initial={{ y: 20, opacity: 0 }}
                                    animate={{ y: 0, opacity: 1 }}
                                    transition={{ delay: 0.2 }}
                                    className="flex gap-8 mt-8"
                                >
                                    {[
                                        { label: 'Followers', value: userData?.followers?.length || 0 },
                                        { label: 'Following', value: userData?.following?.length || 0 },
                                        { label: 'Ideas', value: userData?.publishedIdeas?.length || 0 },
                                        { label: 'Scripts', value: userData?.publishedScripts?.length || 0 }
                                    ].map((stat, index) => (
                                        <motion.div 
                                            key={stat.label}
                                            whileHover={{ y: -2 }}
                                            className="text-center"
                                        >
                                            <div className="text-3xl font-bold text-white">{stat.value}</div>
                                            <div className="text-sm text-gray-400">{stat.label}</div>
                                        </motion.div>
                                    ))}
                                </motion.div>
                            </div>
                        </motion.div>
                    </div>
                </div>

                <div className="bg-[#1A1A1A] min-h-[70vh]">
                    <div className="bg-[#232323] border-b border-[#333333]">
                        <div className="max-w-6xl mx-auto px-4">
                            <div className="flex space-x-8">
                                {['Ideas', 'Scripts', 'Libraries', 'Following', 'Followers'].map((tab, index) => (
                                    <motion.button
                                        key={tab}
                                        initial={{ y: 20, opacity: 0 }}
                                        animate={{ y: 0, opacity: 1 }}
                                        transition={{ delay: 0.1 * index }}
                                        className={`px-6 py-4 text-sm font-medium transition-all ${
                                            activeTab === tab.toLowerCase()
                                                ? 'text-white border-b-2 border-white'
                                                : 'text-gray-400 hover:text-white'
                                        }`}
                                        onClick={() => setActiveTab(tab.toLowerCase())}
                                    >
                                        {tab}
                                    </motion.button>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="p-8">
                        <motion.div 
                            className="bg-[#2A2A2A] rounded-xl p-6"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                        >
                            {activeTab === 'ideas' && (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {userIdeas.length === 0 ? (
                                        <div className="text-gray-400 text-center py-12">
                                            No published ideas yet
                                        </div>
                                    ) : (
                                        userIdeas.map(idea => (
                                            <motion.div
                                                key={idea.id}
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                                className="bg-[#333] rounded-lg p-4"
                                            >
                                                                                                <h3 className="text-xl font-bold mb-2">{idea.title}</h3>
                                                <p className="text-gray-400">{idea.description}</p>
                                                {idea.chartImage && (
                                                    <Image 
                                                        src={idea.chartImage}
                                                        alt="Chart"
                                                        width={400}
                                                        height={300}
                                                        className="mt-4 rounded-lg w-full"
                                                    />
                                                )}
                                                <div className="mt-4 text-sm text-gray-500">
                                                    {new Date(idea.createdAt.toDate()).toLocaleDateString()}
                                                </div>
                                            </motion.div>
                                        ))
                                    )}
                                </div>
                            )}
                        </motion.div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}

