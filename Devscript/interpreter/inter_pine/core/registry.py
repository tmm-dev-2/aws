from .micro_structures import MicroStructuresSyntax
from .patterns import PatternSyntax 
from .technical import TechnicalAnalysis
from .syntax_list import SyntaxList

class Registry:
    def __init__(self):
        self.micro_structures = MicroStructuresSyntax()
        self.patterns = PatternSyntax()
        self.technical = TechnicalAnalysis()
        self.syntax_list = SyntaxList()
        
        # Combine all syntax mappings
        self.function_mappings = {
            **self.micro_structures.syntax_mappings,
            **self.patterns.syntax_mappings,
            **self.technical.functions
        }
        
        # Validate all syntax against the syntax list
        self._validate_syntax()
    
    def get_function(self, name: str):
        """Get function implementation by name"""
        return self.function_mappings.get(name)
    
    def get_category(self, name: str) -> str:
        """Get category for a syntax element"""
        return self.syntax_list.get_category_for_syntax(name)
    
    def list_functions(self) -> list:
        """List all available functions"""
        return list(self.function_mappings.keys())
    
    def list_by_category(self, category: str) -> list:
        """List functions in a specific category"""
        return [name for name in self.function_mappings.keys() 
                if self.get_category(name).startswith(category)]
    
    def _validate_syntax(self):
        """Validate all function mappings against syntax list"""
        valid_syntax = set(self.syntax_list.get_flat_syntax_list())
        mapped_syntax = set(self.function_mappings.keys())
        
        if not mapped_syntax.issubset(valid_syntax):
            invalid = mapped_syntax - valid_syntax
            raise ValueError(f"Invalid syntax mappings found: {invalid}")
