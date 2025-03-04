import React, { useState } from 'react';
import { Tabs } from 'antd';
import EditorLayout from '../app/editor';

export const Workspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState('editor');

  const items = [
    {
      key: 'editor',
      label: 'TMM Editor',
      children: <EditorLayout />
    },
    {
      key: 'screener',
      label: 'Screener',
    },
    {
      key: 'backtester',
      label: 'Backtester',
    }
  ];

  return (
    <div className="workspace">
      <Tabs 
        activeKey={activeTab} 
        onChange={setActiveTab}
        type="card"
        size="large"
        items={items}
      />
    </div>
  );
};
