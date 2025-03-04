import * as monaco from 'monaco-editor';

export const configureMonaco = () => {
  monaco.languages.register({ id: 'devscript' });
  
  monaco.languages.setMonarchTokensProvider('devscript', {
    tokenizer: {
      root: [
        [/[a-zA-Z_]\w*/, {
          cases: {
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }],
        [/[0-9]+/, 'number'],
        [/".*?"/, 'string'],
        [/\/\/.*/, 'comment'],
      ]
    },
    keywords: [
      'indicator', 'strategy', 'library',
      'import', 'export', 'function'
    ]
  });
}
