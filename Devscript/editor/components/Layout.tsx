import React, { useState, useEffect } from 'react';
import { Resizable } from 're-resizable';
import { Layout } from 'antd';
import { FileExplorer } from './FileExplorer';
import { CodeEditor } from './CodeEditor';
import { TopPanel } from './TopPanel';
import { Terminal } from './Terminal';
import { FileOutlined, FolderOutlined } from '@ant-design/icons';
import * as monaco from 'monaco-editor';

const { Content } = Layout;

interface TabType {
  id: string;
  title: string;
  content: string;
  type: 'in' | 'st' | 'lib' | 'py';
}

interface FileType {
  id: string;
  name: string;
  type: 'file' | 'folder';
  children?: FileType[];
}

export const EditorLayout: React.FC = () => {
  const [tabs, setTabs] = useState<TabType[]>([
    { id: '1', title: 'example.in', content: '', type: 'in' }
  ]);
  const [activeTab, setActiveTab] = useState<string>('1');
  const [sidebarWidth, setSidebarWidth] = useState(250);
  const [terminalHeight, setTerminalHeight] = useState(200);
  const [showTerminal, setShowTerminal] = useState(true);
  const [files, setFiles] = useState<FileType[]>([
    {
      id: '1',
      name: 'My Scripts',
      type: 'folder',
      children: [
        { id: '2', name: 'example.in', type: 'file' },
        { id: '3', name: 'strategy.st', type: 'file' }
      ]
    }
  ]);

  const renderFileTree = (items: FileType[]) => {
    return items.map(item => (
      <div key={item.id} className="pl-4">
        <div className="flex items-center gap-2 py-1 px-2 hover:bg-[#37373D] cursor-pointer text-[#CCCCCC]">
          {item.type === 'folder' ? <FolderOutlined /> : <FileOutlined />}
          <span>{item.name}</span>
        </div>
        {item.children && renderFileTree(item.children)}
      </div>
    ));
  };

  return (
    <Layout className="h-screen bg-[#1E1E1E]">
      <TopPanel />
      
      <Layout className="flex-1 overflow-hidden">
        {/* File Explorer */}
        <Resizable
          size={{ width: sidebarWidth, height: '100%' }}
          enable={{ right: true }}
          minWidth={150}
          maxWidth={600}
          onResizeStop={(e, direction, ref, d) => {
            setSidebarWidth(sidebarWidth + d.width);
          }}
          className="bg-[#252526] border-r border-[#1E1E1E]"
        >
          <div className="p-2 text-[#CCCCCC] font-medium border-b border-[#2D2D2D]">
            EXPLORER
          </div>
          <div className="p-2">
            {renderFileTree(files)}
          </div>
        </Resizable>

        {/* Main Editor Area */}
        <Layout className="bg-[#1E1E1E] flex-1">
          {/* Tabs Bar */}
          <div className="flex bg-[#252526] border-b border-[#1E1E1E] h-9">
            {tabs.map(tab => (
              <div 
                key={tab.id}
                className={`px-3 py-1 flex items-center gap-2 cursor-pointer border-r border-[#1E1E1E] ${
                  activeTab === tab.id ? 'bg-[#1E1E1E] text-white' : 'bg-[#2D2D2D] text-[#969696]'
                }`}
                onClick={() => setActiveTab(tab.id)}
              >
                <FileOutlined className="text-xs" />
                <span>{tab.title}</span>
                <button 
                  className="opacity-0 hover:opacity-100 text-[#969696] hover:text-white"
                  onClick={(e) => {
                    e.stopPropagation();
                    setTabs(tabs.filter(t => t.id !== tab.id));
                    if (activeTab === tab.id) {
                      setActiveTab(tabs[0]?.id || '');
                    }
                  }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>

          {/* Editor Content */}
          <Content className="flex-1 overflow-hidden relative">
            <CodeEditor 
              language="javascript"
              theme="vs-dark"
              value={tabs.find(t => t.id === activeTab)?.content || '// Start coding here...'}
              options={{
                minimap: { enabled: true },
                fontSize: 14,
                lineNumbers: 'on',
                roundedSelection: false,
                scrollBeyondLastLine: false,
                automaticLayout: true,
                theme: 'vs-dark',
                wordWrap: 'on',
                formatOnType: true,
                formatOnPaste: true,
                suggestOnTriggerCharacters: true,
                snippetSuggestions: 'inline'
              }}
              onChange={(value) => {
                setTabs(tabs.map(tab => 
                  tab.id === activeTab ? { ...tab, content: value } : tab
                ));
              }}
            />
          </Content>

          {/* Terminal */}
          {showTerminal && (
            <Resizable
              size={{ height: terminalHeight, width: '100%' }}
              enable={{ top: true }}
              minHeight={100}
              maxHeight={500}
              onResizeStop={(e, direction, ref, d) => {
                setTerminalHeight(terminalHeight + d.height);
              }}
              className="bg-[#1E1E1E] border-t border-[#2D2D2D]"
            >
              <div className="flex border-b border-[#2D2D2D] bg-[#252526]">
                <div className="px-3 py-1 text-[#CCCCCC] border-r border-[#2D2D2D]">
                  TERMINAL
                </div>
              </div>
              <Terminal />
            </Resizable>
          )}
        </Layout>

        {/* Chatbot/Documentation Sidebar */}
        <Resizable
          defaultSize={{ width: 300, height: '100%' }}
          enable={{ left: true }}
          minWidth={200}
          maxWidth={800}
          className="bg-[#252526] border-l border-[#1E1E1E]"
        >
          <div className="h-full text-[#CCCCCC]">
            <div className="p-2 font-medium border-b border-[#2D2D2D]">
              AI ASSISTANT
            </div>
            <div className="p-4">
              <div className="bg-[#1E1E1E] p-3 rounded border border-[#2D2D2D]">
                <div className="text-[#569CD6] font-medium">Ask me anything about:</div>
                <ul className="text-[#9CDCFE] mt-2 list-disc list-inside">
                  <li>Trading Strategies</li>
                  <li>Technical Indicators</li>
                  <li>Code Examples</li>
                  <li>Debugging Help</li>
                </ul>
              </div>
              <div className="mt-4 bg-[#1E1E1E] p-3 rounded border border-[#2D2D2D]">
                <div className="text-[#569CD6] font-medium">Quick Actions:</div>
                <div className="mt-2 space-y-2">
                  <button className="w-full text-left px-2 py-1 hover:bg-[#2D2D2D] text-[#9CDCFE] rounded">
                    Generate Strategy Template
                  </button>
                  <button className="w-full text-left px-2 py-1 hover:bg-[#2D2D2D] text-[#9CDCFE] rounded">
                    Debug Current Code
                  </button>
                  <button className="w-full text-left px-2 py-1 hover:bg-[#2D2D2D] text-[#9CDCFE] rounded">
                    Optimize Strategy
                  </button>
                </div>
              </div>
            </div>
          </div>
        </Resizable>
      </Layout>
    </Layout>
  );
};
