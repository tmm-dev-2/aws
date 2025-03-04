from typing import Dict, Any
from env_manager import EnvironmentManager
from language_bridge import LanguageBridge

class UnifiedExecutor:
    def __init__(self):
        self.env_manager = EnvironmentManager()
        self.bridge = self.env_manager.bridge
        
    def execute_mixed(self, code_blocks: Dict[str, str]) -> Dict[str, Any]:
        results = {}
        for lang, code in code_blocks.items():
            results[lang] = self.env_manager.execute_code(
                code, 
                lang,
                {'bridge': self.bridge}
            )
        return results
        
    def execute_devscript(self, code: str) -> Dict[str, Any]:
        blocks = self._parse_language_blocks(code)
        return self.execute_mixed(blocks)
        
    def _parse_language_blocks(self, code: str) -> Dict[str, str]:
        blocks = {}
        current_lang = None
        current_block = []
        
        for line in code.split('\n'):
            if line.startswith('#'):
                lang = line[1:].strip()
                if lang in ['python', 'julia', 'r', 'rust', 'devscript']:
                    if current_lang:
                        blocks[current_lang] = '\n'.join(current_block)
                        current_block = []
                    current_lang = lang
            elif current_lang:
                current_block.append(line)
                
        if current_lang and current_block:
            blocks[current_lang] = '\n'.join(current_block)
            
        return blocks
