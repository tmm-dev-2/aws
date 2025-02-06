import React, { useState } from 'react';
import { MultiSelect } from './MultiSelect';
import { motion, AnimatePresence } from 'framer-motion';

interface PostIdeaModalProps {
  onClose: () => void;
  onPost: (data: { 
    title: string; 
    description: string; 
    categories: string[];
    market: string;
    tools: string[];
  }) => Promise<void>;
  previewImage: string | null;
  categories: string[];
  markets: string[];
  tools: {
    technical: string[];
    fundamental: string[];
  };
}

export function PostIdeaModal({ onClose, onPost, previewImage, categories, markets, tools }: PostIdeaModalProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedMarket, setSelectedMarket] = useState('');
  const [selectedTools, setSelectedTools] = useState<string[]>([]);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description || !selectedMarket) return;

    await onPost({ 
      title, 
      description, 
      categories: selectedCategories,
      market: selectedMarket,
      tools: selectedTools
    });
    setShowSuccess(true);
    setTimeout(() => {
      onClose();
    }, 2000);
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
      <AnimatePresence>
        {showSuccess && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="absolute top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg"
          >
            Post published successfully!
          </motion.div>
        )}
      </AnimatePresence>
      <div className="bg-[#242424] p-6 rounded-lg w-[800px] max-h-[90vh] overflow-y-auto">
        <h2 className="text-2xl font-bold text-white mb-4">Share Trading Idea</h2>
        
        {previewImage && (
          <div className="mb-4 rounded overflow-hidden">
            <img src={previewImage} alt="Chart Preview" className="w-full" />
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Title"
            className="w-full bg-[#1a1a1a] text-white p-2 rounded mb-4"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          
          <textarea
            placeholder="Description"
            className="w-full bg-[#1a1a1a] text-white p-2 rounded mb-4 h-32"
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
            className="w-full bg-[#1a1a1a] text-white p-2 rounded my-4"
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
            placeholder="Select Trading Tools"
          />

          <div className="flex justify-end gap-3 mt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded bg-gray-600 text-white"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded bg-blue-500 text-white"
            >
              Post Idea
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}