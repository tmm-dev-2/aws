import React, { useState } from 'react';

interface CreateWatchlistPopupProps {
  onClose: () => void;
  onCreate: (name: string) => void;
}

const CreateWatchlistPopup: React.FC<CreateWatchlistPopupProps> = ({ onClose, onCreate }) => {
  const [newListName, setNewListName] = useState('');

  const handleCreate = () => {
    onCreate(newListName);
    onClose();
  };

  return (
    <div className="fixed top-0 left-0 w-full h-full bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-8 rounded">
        <h2 className="text-lg font-bold mb-4">Create New Watchlist</h2>
        <input
          type="text"
          placeholder="Enter list name"
          className="border p-2 mb-4 w-full"
          value={newListName}
          onChange={(e) => setNewListName(e.target.value)}
        />
        <div className="flex justify-end">
          <button className="bg-gray-300 p-2 rounded mr-2" onClick={onClose}>
            Cancel
          </button>
          <button className="bg-blue-500 text-white p-2 rounded" onClick={handleCreate}>
            Create
          </button>
        </div>
      </div>
    </div>
  );
};

interface Watchlist {
  name: string;
}

const WatchlistPage = () => {
  const [isCreatePopupVisible, setIsCreatePopupVisible] = useState(false);
  const [watchlists, setWatchlists] = useState<Watchlist[]>([]);

  const handleCreateClick = () => {
    setIsCreatePopupVisible(true);
  };

  const handleCreateWatchlist = (name: string) => {
    // Implement logic to create a new watchlist
    console.log('Creating watchlist:', name);
    setWatchlists([...watchlists, { name }]);
  };

  const handleClosePopup = () => {
    setIsCreatePopupVisible(false);
  };

  return (
    <div>
      <h1>Watchlist</h1>
      <button onClick={handleCreateClick}>Create New List</button> {/* Assuming this button exists */}

      {isCreatePopupVisible && (
        <CreateWatchlistPopup onClose={handleClosePopup} onCreate={handleCreateWatchlist} />
      )}

      {/* Existing watchlist display logic */}
    </div>
  );
};

export default WatchlistPage;
