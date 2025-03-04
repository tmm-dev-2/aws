import React, { useRef, useEffect, useState } from 'react';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuSeparator } from './ui/dropdown-menu';
import { FaPlay, FaTrash, FaSave } from 'react-icons/fa';
import { ChevronDown, CloudUpload, Pencil, Plus, FolderArchive, Copy, MoreHorizontal } from 'lucide-react';
import * as monaco from 'monaco-editor';
import '../monaco-config';
import '../monaco-languages';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc, updateDoc, doc, getDoc, getDocs, where, query } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET!,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID!,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID!
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const RenameDialog = ({ isOpen, onClose, onSave, initialName }: {
  isOpen: boolean;
  onClose: () => void;
  onSave: (name: string) => void;
  initialName: string;
}) => {
  const [name, setName] = useState(initialName);

  return isOpen ? (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-[#2D2D2D] rounded-lg p-4 w-96">
        <h3 className="text-white mb-4">Rename Script</h3>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full bg-[#1E1E1E] text-white rounded px-2 py-1 mb-4"
          autoFocus
        />
        <div className="flex justify-end space-x-2">
          <button 
            onClick={onClose}
            className="px-4 py-2 text-white hover:bg-[#3D3D3D] rounded"
          >
            Cancel
          </button>
          <button 
            onClick={() => onSave(name)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  ) : null;
};

interface Script {
  id?: string;
  name: string;
  content: string;
  type: 'indicator' | 'strategy' | 'library';
  isPublished: boolean;
  authorId: string;
  settings?: ScriptSettings;
  createdAt: Date;
  updatedAt: Date;
}

interface ScriptSettings {
  inputs: Record<string, any>;
  style?: Record<string, any>;
  visibility?: boolean;
}

interface ScriptEditorProps {
  onRunScript: (script: string, chartData: any) => void;
  userId: string;
  chartData?: any;
}

const ScriptEditor: React.FC<ScriptEditorProps> = ({ onRunScript, userId, chartData }) => {
  const [currentScript, setCurrentScript] = useState<Script | null>(null);
  const [scriptType, setScriptType] = useState<'indicator' | 'strategy' | 'library'>('indicator');
  const [scriptName, setScriptName] = useState('Untitled Script');
  const [scripts, setScripts] = useState<Script[]>([]);
  const [showSettings, setShowSettings] = useState(false);
  const [showRenameDialog, setShowRenameDialog] = useState(false);
  
  const editorRef = useRef<HTMLDivElement>(null);
  const monacoRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);

  useEffect(() => {
    if (editorRef.current) {
      monacoRef.current = monaco.editor.create(editorRef.current, {
        value: '',
        language: 'typescript',
        theme: 'vs-dark',
        minimap: { enabled: false },
        fontSize: 14,
        automaticLayout: true,
        scrollBeyondLastLine: false,
        lineNumbers: 'on',
        roundedSelection: false,
        contextmenu: true,
        renderLineHighlight: 'all',
        scrollbar: {
          vertical: 'visible',
          horizontal: 'visible',
          useShadows: false,
          verticalScrollbarSize: 10,
          horizontalScrollbarSize: 10
        }
      });

      return () => {
        if (monacoRef.current) {
          monacoRef.current.dispose();
        }
      };
    }
  }, []);

  useEffect(() => {
    if (userId) {
      loadUserScripts();
    }
  }, [userId]);

  const loadUserScripts = async () => {
    if (!userId) return;
    const scriptsRef = collection(db, 'scripts');
    const userScriptsQuery = query(scriptsRef, where('authorId', '==', userId));
    const querySnapshot = await getDocs(userScriptsQuery);
    const loadedScripts = querySnapshot.docs.map(doc => ({ ...doc.data(), id: doc.id } as Script));
    setScripts(loadedScripts);
  };

  const saveScript = async () => {
    if (!monacoRef.current || !userId) return;
    
    const content = monacoRef.current.getValue();
    const scriptsRef = collection(db, 'scripts');
    
    const scriptData: Script = {
      name: scriptName,
      content,
      type: scriptType,
      isPublished: false,
      authorId: userId,
      createdAt: new Date(),
      updatedAt: new Date(),
      settings: {
        inputs: {},
        style: {},
        visibility: true
      }
    };

    if (currentScript?.id) {
      await updateDoc(doc(db, 'scripts', currentScript.id), {
        ...scriptData,
        createdAt: currentScript.createdAt
      });
    } else {
      const docRef = await addDoc(scriptsRef, scriptData);
      setCurrentScript({ ...scriptData, id: docRef.id });
    }
    await loadUserScripts();
  };

  const loadScript = async (scriptId: string) => {
    const scriptDoc = await getDoc(doc(db, 'scripts', scriptId));
    if (scriptDoc.exists()) {
      const scriptData = scriptDoc.data() as Script;
      setCurrentScript({ ...scriptData, id: scriptDoc.id });
      setScriptName(scriptData.name);
      setScriptType(scriptData.type);
      monacoRef.current?.setValue(scriptData.content);
    }
  };

  const handleRename = async (newName: string) => {
    if (!currentScript?.id) return;
    await updateDoc(doc(db, 'scripts', currentScript.id), {
      name: newName,
      updatedAt: new Date()
    });
    setScriptName(newName);
    setShowRenameDialog(false);
    await loadUserScripts();
  };

  const createNewScript = () => {
    setCurrentScript(null);
    setScriptName('Untitled Script');
    monacoRef.current?.setValue('');
  };

  const handleRunScript = async () => {
    const script = monacoRef.current?.getValue() || '';
    try {
      const response = await fetch('http://localhost:5001/run_script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          script,
          type: scriptType,
          settings: currentScript?.settings,
          data: chartData
        })
      });
      const result = await response.json();
      onRunScript(script, {
        name: scriptName,
        type: scriptType,
        settings: currentScript?.settings,
        data: result
      });
    } catch (error) {
      console.error('Error running script:', error);
    }
  };

  const handleClear = () => {
    monacoRef.current?.setValue('');
    setCurrentScript(null);
    setScriptName('Untitled Script');
  };

  const handleMakeCopy = async () => {
    if (!currentScript || !userId) return;
    const copyData: Script = {
      ...currentScript,
      name: `${currentScript.name} (Copy)`,
      isPublished: false,
      createdAt: new Date(),
      updatedAt: new Date(),
      authorId: userId
    };
    delete copyData.id;
    const docRef = await addDoc(collection(db, 'scripts'), copyData);
    setCurrentScript({ ...copyData, id: docRef.id });
    setScriptName(copyData.name);
    await loadUserScripts();
  };

  const toggleSettings = () => {
    setShowSettings(!showSettings);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="bg-[#1E1E1E] rounded-lg shadow-lg">
        <div className="flex items-center justify-between p-2 bg-[#1E1E1E] rounded-t-lg">
          <div className="flex space-x-2">
            <button 
              className="p-0.5 bg-[#1E1E1E] text-white rounded flex flex-col items-center text-sm"
              onClick={() => setShowRenameDialog(true)}
            >
              <span>{scriptName}</span>
              <span className="text-blue-500 text-xs">
                {currentScript?.id ? 'Saved' : 'Unsaved'}
              </span>
            </button>
            
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="p-2 bg-[#1E1E1E] text-white rounded flex items-center text-sm">
                  <ChevronDown className="h-4 w-4"/>
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56 bg-[#2D2D2D] text-white" side="bottom">
                <button onClick={saveScript} className="w-full text-left p-2 hover:bg-[#3D3D3D] flex items-center">
                  <CloudUpload className="h-4 w-4 mr-2"/>Save script
                </button>
                <button onClick={handleMakeCopy} className="w-full text-left p-2 hover:bg-[#3D3D3D] flex items-center">
                  <Copy className="h-4 w-4 mr-2"/>Make a copy
                </button>
                <button onClick={() => setShowRenameDialog(true)} className="w-full text-left p-2 hover:bg-[#3D3D3D] flex items-center">
                  <Pencil className="h-4 w-4 mr-2"/>Rename
                </button>
                <DropdownMenuSeparator />
                <button onClick={createNewScript} className="w-full text-left p-2 hover:bg-[#3D3D3D] flex items-center">
                  <Plus className="h-4 w-4 mr-2"/>Create new
                </button>
                <DropdownMenuSeparator />
                <select
                  value={scriptType}
                  onChange={(e) => setScriptType(e.target.value as any)}
                  className="w-full p-2 bg-[#2D2D2D] text-white"
                >
                  <option value="indicator">Indicator</option>
                  <option value="strategy">Strategy</option>
                  <option value="library">Library</option>
                </select>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          
          <div className="flex space-x-2">
            <button onClick={handleRunScript} className="p-2 text-white rounded flex items-center text-sm hover:bg-[#2D2D2D]">
              <FaPlay className="mr-1" /> Run
            </button>
            <button onClick={handleClear} className="p-2 text-white rounded flex items-center text-sm hover:bg-[#2D2D2D]">
              <FaTrash className="mr-1" /> Clear
            </button>
            <button onClick={saveScript} className="p-2 text-white rounded flex items-center text-sm hover:bg-[#2D2D2D]">
              <FaSave className="mr-1" /> Save
            </button>
            <button onClick={toggleSettings} className="p-2 text-white rounded flex items-center text-sm hover:bg-[#2D2D2D]">
              <MoreHorizontal className="mr-1" />
            </button>
          </div>
        </div>
        <div ref={editorRef} style={{ height: '500px', width: '100%' }} />
      </div>
      
      {showSettings && (
        <div className="bg-[#1E1E1E] mt-2 p-4 rounded-lg">
          <h3 className="text-white mb-4">Script Settings</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-white text-sm">Visibility</label>
              <input
                type="checkbox"
                checked={currentScript?.settings?.visibility}
                onChange={(e) => {
                  if (currentScript) {
                    setCurrentScript({
                      ...currentScript,
                      settings: {
                        ...currentScript.settings,
                        visibility: e.target.checked
                      }
                    });
                  }
                }}
                className="ml-2"
              />
            </div>
          </div>
        </div>
      )}

      <RenameDialog
        isOpen={showRenameDialog}
        onClose={() => setShowRenameDialog(false)}
        onSave={handleRename}
        initialName={scriptName}
      />
    </div>
  );
};

export default ScriptEditor;
