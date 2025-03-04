import React from 'react';
import { Button, Dropdown, Menu } from 'antd';
import { 
  FileOutlined, 
  PlayCircleOutlined, 
  SaveOutlined, 
  SettingOutlined,
  FolderOutlined,
  CodeOutlined,
  EyeOutlined,
  TerminalOutlined,
  CloudUploadOutlined,
  CopyOutlined,
  EditOutlined
} from '@ant-design/icons';
import { ChevronDown } from 'lucide-react';

interface TopPanelProps {
  onRun: () => void;
  onNewFile: (type: 'in' | 'st' | 'lib' | 'py') => void;
}

export const TopPanel: React.FC<TopPanelProps> = ({ onRun, onNewFile }) => {
  const fileMenuItems = [
    {
      key: 'new',
      label: 'New File',
      children: [
        {
          key: 'indicator',
          label: 'Indicator (.in)',
          onClick: () => onNewFile('in')
        },
        {
          key: 'strategy',
          label: 'Strategy (.st)',
          onClick: () => onNewFile('st')
        },
        {
          key: 'library',
          label: 'Library (.lib)',
          onClick: () => onNewFile('lib')
        },
        {
          key: 'python',
          label: 'Python File (.py)',
          onClick: () => onNewFile('py')
        }
      ]
    },
    {
      key: 'open',
      label: 'Open File...'
    },
    {
      key: 'save',
      label: 'Save'
    },
    {
      key: 'saveAs',
      label: 'Save As...'
    }
  ];

  const viewMenuItems = [
    {
      key: 'split',
      label: 'Split Editor'
    },
    {
      key: 'terminal',
      label: 'Toggle Terminal'
    },
    {
      key: 'explorer',
      label: 'Show Explorer'
    }
  ];

  return (
    <div className="flex flex-col">
      {/* VS Code style top menu */}
      <div className="flex items-center gap-2 p-1 bg-[#1E1E1E] border-b border-gray-800">
        <Dropdown menu={{ items: fileMenuItems }}>
          <Button type="text" className="text-white">File</Button>
        </Dropdown>
        <Button type="text" className="text-white">Edit</Button>
        <Dropdown menu={{ items: viewMenuItems }}>
          <Button type="text" className="text-white">View</Button>
        </Dropdown>
        <Button type="text" className="text-white">Run</Button>
        <Button type="text" className="text-white">Terminal</Button>
        <Button type="text" className="text-white">Help</Button>
      </div>

      {/* PineScript style script management */}
      <div className="flex items-center justify-between p-2 bg-[#1E1E1E] border-b border-gray-700">
        <div className="flex space-x-2">
          <button className="p-0.5 bg-[#1E1E1E] text-white rounded flex flex-col items-center text-sm">
            <span>Untitled Script</span>
            <span className="text-blue-500 text-xs">Save</span>
          </button>
          <Dropdown menu={{ 
            items: [
              {
                key: 'save',
                label: 'Save script',
                icon: <CloudUploadOutlined />
              },
              {
                key: 'copy',
                label: 'Make a copy...',
                icon: <CopyOutlined />
              },
              {
                key: 'rename',
                label: 'Rename...',
                icon: <EditOutlined />
              }
            ]
          }}>
            <Button type="text">
              <ChevronDown className="h-4 w-4 text-white"/>
            </Button>
          </Dropdown>
        </div>

        <div className="flex space-x-2">
          <Button 
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={onRun}
          >
            Run
          </Button>
          <Button 
            icon={<SaveOutlined />}
            className="text-white"
          >
            Save
          </Button>
          <Button 
            icon={<SettingOutlined />}
            className="text-white"
          >
            Settings
          </Button>
        </div>
      </div>
    </div>
  );
};
