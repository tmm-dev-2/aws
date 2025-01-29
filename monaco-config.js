import * as monaco from 'monaco-editor';

self.MonacoEnvironment = {
  getWorkerUrl: function (moduleId, label) {
    if (label === 'typescript' || label === 'javascript' || label === 'devscript') {
      return '/_next/static/chunks/ts.worker.js';
    }
    return '/_next/static/chunks/editor.worker.js';
  }
};
