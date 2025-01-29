import React, { useRef, useEffect } from 'react';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuSeparator } from './ui/dropdown-menu';
import { FaPlay, FaTrash, FaSave } from 'react-icons/fa';
import { ChevronDown, CloudUpload, Pencil, Plus, FolderArchive, Copy, MoreHorizontal } from 'lucide-react';
import * as monaco from 'monaco-editor';
import '../monaco-config'; // Import the Monaco configuration
import '../monaco-languages';

interface ScriptEditorProps {
  onRunScript: (script: string) => void;
}

const ScriptEditor: React.FC<ScriptEditorProps> = ({ onRunScript }) => {
  const editorRef = useRef<HTMLDivElement>(null);
  const monacoRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);

  useEffect(() => {
    let isEditorMounted = false;

    const initMonaco = async () => {
      try {
        if (editorRef.current && !isEditorMounted) {
          isEditorMounted = true;
          const monaco = await import('monaco-editor');

          if (!monacoRef.current) {
            monaco.editor.defineTheme('custom-dark', {
              base: 'vs-dark',
              inherit: true,
              rules: [
                { token: '', background: '1E1E1E' },
                { token: 'comment', foreground: '6A9955' },
                { token: 'keyword', foreground: '569CD6' },
                { token: 'string', foreground: 'CE9178' },
                { token: 'number', foreground: 'B5CEA8' },
              ],
              colors: {
                'editor.background': '#1E1E1E',
                'editor.foreground': '#D4D4D4',
                'editor.lineHighlightBackground': '#2D2D2D',
                'editorCursor.foreground': '#AEAFAD',
                'editorWhitespace.foreground': '#3B3A32',
                'editorIndentGuide.background': '#404040',
                'editorIndentGuide.activeBackground': '#707070',
              },
            });

            monacoRef.current = monaco.editor.create(editorRef.current, {
              value: '',
              language: 'devscript',
              theme: 'custom-dark',
            });
          }
        }
      } catch (error) {
        console.error("Error initializing Monaco Editor:", error);
      }
    };

    initMonaco();

    return () => {
      isEditorMounted = false;
      if (monacoRef.current) {
        monacoRef.current.dispose();
        monacoRef.current = null;
      }
    };
  }, []);
  const handleRunScript = () => {
    const script = monacoRef.current?.getValue() || '';
    fetch('http://localhost:5001/run_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            onRunScript(data.data);
        } else {
            console.error('Script execution failed:', data.message);
        }
    })
    .catch(error => {
        console.error('Error running script:', error);
    });
  };


  const handleClear = () => {
    monacoRef.current?.setValue('');
  };

  const handleSave = () => {
    const script = monacoRef.current?.getValue() || '';
    console.log('Script saved:', script);
    // Implement save functionality here
  };

  return (
    <div className="bg-[#1E1E1E] rounded-lg shadow-lg">
      <div className="flex items-center justify-between p-2 bg-[#1E1E1E] rounded-t-lg">
        <div className="flex space-x-2 justify-between">
          <button className="p-0.5 bg-[#1E1E1E] text-white rounded flex flex-col items-center text-sm">
            <span>Untitled Script </span>
            <span className="text-blue-500 text-xs items-right">Save</span>
          </button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="p-2 bg-[#1E1E1E] text-white rounded flex flex-col items-center text-sm">
                <span> <ChevronDown className="h-4 w-4"/></span>
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" side="bottom">
              <button className="w-full text-left p-2 hover:bg-gray-100 block"><CloudUpload className="h-4 w-4"/>Save script</button>
              <button className="w-full text-left p-2 hover:bg-gray-100 block"><Copy className="h-4 w-4"/>Make a copy...</button>
              <button className="w-full text-left p-2 hover:bg-gray-100 block"><Pencil className="h-4 w-4"/>Rename...</button>
              <DropdownMenuSeparator />
              <button className="w-full text-left p-2 hover:bg-gray-100 block"><Plus className="h-4 w-4"/>Create new</button>
              <DropdownMenuSeparator />
              <button className="w-full text-left p-2 hover:bg-gray-100 block"><FolderArchive className="h-4 w-4"/>Open script...</button>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <div className="flex space-x-2">
          <button onClick={handleRunScript} className="p-2 bg-blue-500 text-white rounded flex items-center text-sm">
            <FaPlay className="mr-1" /> Run
          </button>
          <button onClick={handleClear} className="p-2 bg-gray-500 text-white rounded flex items-center text-sm">
            <FaTrash className="mr-1" /> Clear
          </button>
          <button onClick={handleSave} className="p-2 bg-green-500 text-white rounded flex items-center text-sm">
            <FaSave className="mr-1" /> Save
          </button>
          <button className="p-2 text-white rounded flex items-center text-sm">
            <MoreHorizontal className="mr-1" /> 
          </button>
        </div>
      </div>
      <div ref={editorRef} style={{ height: '200px', width: '100%' }}></div>
    </div>
  );
};

export default ScriptEditor;