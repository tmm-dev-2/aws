class ParserError(Exception):
    """Custom exception for parser errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class TokenizerError(Exception):
    """Custom exception for tokenizer errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InterpreterError(Exception):
    """Custom exception for interpreter errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
