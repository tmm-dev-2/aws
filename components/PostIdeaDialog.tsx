import React, { useState } from 'react';
import { MultiSelect } from './MultiSelect';
import { useAuth } from '../context/AuthContext';
import { storage, db } from '../firebase/config';
import { collection, addDoc } from 'firebase/firestore';
import { ref, uploadString } from 'firebase/storage';
import html2canvas from 'html2canvas';
import { Dialog as HeadlessDialog } from '@headlessui/react';


interface PostIdeaDialogProps {
  onClose: () => void;
  categories: string[];
  markets: string[];
  tools: {
    technical: string[];
    fundamental: string[];
  };
}

export default function PostIdeaDialog({ onClose, categories, markets, tools }: PostIdeaDialogProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedMarket, setSelectedMarket] = useState('');
  const [selectedTools, setSelectedTools] = useState<string[]>([]);
  const { user } = useAuth();

  const captureChart = async () => {
    const chartElement = document.querySelector('#tradingview_chart');
    if (chartElement) {
      const canvas = await html2canvas(chartElement);
      return canvas.toDataURL('image/png');
    }
    return null;
  };

  const handlePost = async () => {
    const chartImage = await captureChart();
    if (!chartImage) return;

    const imageRef = ref(storage, `charts/${Date.now()}-chart.png`);
    await uploadString(imageRef, chartImage, 'data_url');
    const imageUrl = await getDownloadURL(imageRef);

    await addDoc(collection(db, 'ideas'), {
      title,
      description,
      chartImage: imageUrl,
      categories: selectedCategories,
      market: selectedMarket,
      tools: selectedTools,
      author: {
        id: user?.uid,
        name: user?.displayName,
        avatar: user?.photoURL
      },
      createdAt: new Date(),
      likes: 0,
      reactions: {},
      comments: []
    });

    onClose();
  };

  return (
    <HeadlessDialog open={true} onClose={onClose} className="fixed inset-0 z-50">
      <div className="flex items-center justify-center min-h-screen p-4">
        <HeadlessDialog.Overlay className="fixed inset-0 bg-black/50" />
        
        <div className="relative bg-[#242424] p-6 rounded-lg w-full max-w-md">
          <HeadlessDialog.Title className="text-xl font-bold text-white mb-4">
            Post Trading Idea
          </HeadlessDialog.Title>
          
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Title"
              className="w-full bg-[#1a1a1a] text-white p-2 rounded"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />

            <textarea
              placeholder="Description"
              className="w-full bg-[#1a1a1a] text-white p-2 rounded h-32"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />

            <MultiSelect
              options={categories}
              value={selectedCategories}
              onChange={setSelectedCategories}
              placeholder="Select Categories"
            />

            <select
              value={selectedMarket}
              onChange={(e) => setSelectedMarket(e.target.value)}
              className="w-full bg-[#1a1a1a] text-white p-2 rounded"
            >
              <option value="">Select Market</option>
              {markets.map(market => (
                <option key={market} value={market}>{market}</option>
              ))}
            </select>

            <MultiSelect
              options={[...tools.technical, ...tools.fundamental]}
              value={selectedTools}
              onChange={setSelectedTools}
              placeholder="Select Tools Used"
            />

            <div className="flex justify-end gap-2 mt-6">
              <button
                onClick={onClose}
                className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded"
              >
                Cancel
              </button>
              <button
                onClick={handlePost}
                className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded"
              >
                Post
              </button>
            </div>
          </div>
        </div>
      </div>
    </HeadlessDialog>
  );
}
