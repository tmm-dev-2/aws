from enum import Enum
from typing import List, Optional
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
    EQUAL = "="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="
    
    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"
    
    # Keywords
    IF = "if"
    ELSE = "else"
    FOR = "for"
    WHILE = "while"
    RETURN = "return"
    BREAK = "break"
    CONTINUE = "continue"
    VAR = "var"
    TRUE = "true" 
    FALSE = "false"
    AND = "and"
    OR = "or"
    NOT = "not"
    
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int = 1
    column: int = 1

class NodeType(Enum):
    PROGRAM = "PROGRAM"
    BLOCK = "BLOCK"
    EXPRESSION = "EXPRESSION"
    BINARY_OP = "BINARY_OP"
    UNARY_OP = "UNARY_OP"
    LITERAL = "LITERAL"
    IDENTIFIER = "IDENTIFIER"
    ASSIGNMENT = "ASSIGNMENT"
    FUNCTION_CALL = "FUNCTION_CALL"
    IF_STATEMENT = "IF_STATEMENT"
    WHILE_STATEMENT = "WHILE_STATEMENT"
    FOR_STATEMENT = "FOR_STATEMENT"
    RETURN_STATEMENT = "RETURN_STATEMENT"
    VARIABLE_DECL = "VARIABLE_DECL"
    ARRAY_ACCESS = "ARRAY_ACCESS"
    MEMBER_ACCESS = "MEMBER_ACCESS"

class ASTNode:
    def __init__(self, type: NodeType, value=None, children=None, token=None):
        self.type = type
        self.value = value
        self.children = children if children else []
        self.token = token
        self.line = token.line if token else 0
        self.column = token.column if token else 0

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.had_error = False
        self.errors = []

    def parse(self) -> ASTNode:
        try:
            statements = []
            while not self.is_at_end():
                stmt = self.declaration()
                if stmt:
                    statements.append(stmt)
            return ASTNode(NodeType.PROGRAM, children=statements)
        except Exception as e:
            self.had_error = True
            self.errors.append(str(e))
            return None

    def declaration(self) -> Optional[ASTNode]:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except Exception as e:
            self.synchronize()
            return None

    def var_declaration(self) -> ASTNode:
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
            
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return ASTNode(NodeType.VARIABLE_DECL, name.value, [initializer] if initializer else [], name)

    def statement(self) -> ASTNode:
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.BREAK):
            return self.break_statement()
        if self.match(TokenType.CONTINUE):
            return self.continue_statement()
        if self.match(TokenType.LBRACE):
            return self.block()
        return self.expression_statement()

    def if_statement(self) -> ASTNode:
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after if condition")
        
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
            
        return ASTNode(NodeType.IF_STATEMENT, children=[condition, then_branch, else_branch])

    def while_statement(self) -> ASTNode:
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after while condition")
        body = self.statement()
        
        return ASTNode(NodeType.WHILE_STATEMENT, children=[condition, body])

    def for_statement(self) -> ASTNode:
        self.consume(TokenType.LPAREN, "Expected '(' after 'for'")
        
        initializer = None
        if not self.match(TokenType.SEMICOLON):
            if self.match(TokenType.VAR):
                initializer = self.var_declaration()
            else:
                initializer = self.expression_statement()
                
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after loop condition")
        
        increment = None
        if not self.check(TokenType.RPAREN):
            increment = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after for clauses")
        
        body = self.statement()
        
        return ASTNode(NodeType.FOR_STATEMENT, children=[initializer, condition, increment, body])

    def block(self) -> ASTNode:
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.declaration())
            
        self.consume(TokenType.RBRACE, "Expected '}' after block")
        return ASTNode(NodeType.BLOCK, children=statements)

    def expression_statement(self) -> ASTNode:
        expr = self.expression()

        # Handle optional semicolon
        if self.match(TokenType.SEMICOLON):
            pass
    
        return expr

    def expression(self) -> ASTNode:
        return self.assignment()

    def assignment(self) -> ASTNode:
        expr = self.or_expr()
        
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            
            if expr.type == NodeType.IDENTIFIER:
                return ASTNode(NodeType.ASSIGNMENT, expr.value, [value], equals)
            elif expr.type == NodeType.MEMBER_ACCESS:
                return ASTNode(NodeType.ASSIGNMENT, "member", [expr, value], equals)
            elif expr.type == NodeType.ARRAY_ACCESS:
                return ASTNode(NodeType.ASSIGNMENT, "array", [expr, value], equals)
                
            self.error(equals, "Invalid assignment target")
            
        return expr

    def or_expr(self) -> ASTNode:
        expr = self.and_expr()
        
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = ASTNode(NodeType.BINARY_OP, operator.value, [expr, right], operator)
            
        return expr

    def and_expr(self) -> ASTNode:
        expr = self.equality()
        
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = ASTNode(NodeType.BINARY_OP, operator.value, [expr, right], operator)
            
        return expr

    def equality(self) -> ASTNode:
        expr = self.comparison()
        
        while self.match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = ASTNode(NodeType.BINARY_OP, operator.value, [expr, right], operator)
            
        return expr

    def comparison(self) -> ASTNode:
        expr = self.term()
        
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, 
                        TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = ASTNode(NodeType.BINARY_OP, operator.value, [expr, right], operator)
            
        return expr

    def term(self) -> ASTNode:
        expr = self.factor()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = ASTNode(NodeType.BINARY_OP, operator.value, [expr, right], operator)
            
        return expr

    def factor(self) -> ASTNode:
        expr = self.unary()
        
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = ASTNode(NodeType.BINARY_OP, operator.value, [expr, right], operator)
            
        return expr

    def unary(self) -> ASTNode:
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return ASTNode(NodeType.UNARY_OP, operator.value, [right], operator)
            
        return self.call()

    def call(self) -> ASTNode:
        expr = self.primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expected property name after '.'")
                expr = ASTNode(NodeType.MEMBER_ACCESS, name.value, [expr], name)
            elif self.match(TokenType.LBRACKET):
                index = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after array index")
                expr = ASTNode(NodeType.ARRAY_ACCESS, children=[expr, index])
            else:
                break
                
        return expr

    def finish_call(self, callee: ASTNode) -> ASTNode:
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            while True:
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
                    
        paren = self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        return ASTNode(NodeType.FUNCTION_CALL, callee.value, arguments, paren)
    
    def primary(self) -> ASTNode:
        if self.match(TokenType.NUMBER):
            token = self.previous()
            return ASTNode(NodeType.LITERAL, float(token.value), token=token)

        if self.match(TokenType.STRING, TokenType.STRING_INTERPOLATED):
            token = self.previous()
            return ASTNode(NodeType.LITERAL, str(token.value), token=token)

        if self.match(TokenType.TRUE):
            return ASTNode(NodeType.LITERAL, True, token=self.previous())

        if self.match(TokenType.FALSE):
            return ASTNode(NodeType.LITERAL, False, token=self.previous())

        if self.match(TokenType.IDENTIFIER):
            return ASTNode(NodeType.IDENTIFIER, self.previous().value, token=self.previous())

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        raise self.error(self.peek(), "Expected expression")

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        error = f"Line {token.line}, Column {token.column}: {message}"
        if token.type == TokenType.EOF:
            error = f"{error} at end"
        else:
            error = f"{error} at '{token.value}'"
        self.had_error = True
        self.errors.append(error)
        return SyntaxError(error)

    def synchronize(self):
        self.advance()
        
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
                
            if self.peek().type in {
                TokenType.IF,
                TokenType.WHILE,
                TokenType.FOR,
                TokenType.RETURN,
                TokenType.VAR
            }:
                return
                
            self.advance()
