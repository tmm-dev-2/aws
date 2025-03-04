from typing import List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER" 
    SYNTAX = "SYNTAX"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    EQUAL = "="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="
    AND = "and"
    OR = "or"
    NOT = "not"
    
    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"
    COLON = ":"
    
    # Keywords
    IF = "if"
    ELSE = "else"
    FOR = "for"
    WHILE = "while"
    BREAK = "break"
    CONTINUE = "continue"
    RETURN = "return"
    VAR = "var"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    
    # Special
    EOF = "EOF"
    NEWLINE = "NEWLINE"
    STRING_INTERPOLATED = "STRING_INTERPOLATED"

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class Tokenizer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR, 
            'while': TokenType.WHILE,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'return': TokenType.RETURN,
            'var': TokenType.VAR,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'null': TokenType.NULL,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT
        }
        
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '%': TokenType.PERCENT,
            '=': TokenType.EQUAL,
            '>': TokenType.GREATER,
            '<': TokenType.LESS,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            ';': TokenType.SEMICOLON,
            ':': TokenType.COLON
        }

        self.two_char_operators = {
            '==': TokenType.EQUAL_EQUAL,
            '!=': TokenType.NOT_EQUAL,
            '>=': TokenType.GREATER_EQUAL,
            '<=': TokenType.LESS_EQUAL
        }

    def tokenize(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
            
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        
        if c.isspace():
            if c == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return

        if c.isdigit() or (c == '-' and self.peek().isdigit()):
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        elif c in ['"', "'"]:
            self.string(c)
        else:
            self.operator_or_delimiter(c)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        # Handle decimals
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        # Handle scientific notation
        if self.peek() in ['e', 'E']:
            e_pos = self.current
            self.advance()
            if self.peek() in ['+', '-']:
                self.advance()
            if not self.peek().isdigit():
                self.current = e_pos
            else:
                while self.peek().isdigit():
                    self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type, text)

    def string(self, quote: str):
        is_interpolated = False
        
        while self.peek() != quote and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            elif self.peek() == '\\':
                self.advance()
            elif self.peek() == '{' and self.peek_next() == '{':
                is_interpolated = True
                self.advance()
                self.advance()
            self.advance()

        if self.is_at_end():
            raise SyntaxError(f"Unterminated string at line {self.line}")

        self.advance()  # Closing quote
        
        # Get string value without quotes
        value = self.source[self.start + 1:self.current - 1]
        token_type = TokenType.STRING_INTERPOLATED if is_interpolated else TokenType.STRING
        self.add_token(token_type, value)

    def operator_or_delimiter(self, c: str):
        if c == ';':
            self.add_token(TokenType.SEMICOLON, c)
            return
            
        if c in self.operators:
            # Check for two-character operators
            if self.peek() == '=' and c in ['=', '!', '>', '<']:
                self.advance()
                two_char = c + '='
                self.add_token(self.two_char_operators[two_char], two_char)
            else:
                self.add_token(self.operators[c], c)
        else:
            raise SyntaxError(f"Unexpected character '{c}' at line {self.line}")
    

    def add_token(self, type: TokenType, value: Any):
        self.tokens.append(Token(type, value, self.line, self.column))
        self.column += len(str(value))

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def peek(self) -> str:
        return '\0' if self.is_at_end() else self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def get_token_at(self, index: int) -> Optional[Token]:
        return self.tokens[index] if 0 <= index < len(self.tokens) else None
