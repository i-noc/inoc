from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List, Optional

class TokenType(Enum):
    # Símbolos
    SLASH = auto()        # /
    SLASH_COLON = auto()  # /:
    SLASH_PLUS = auto()   # /+
    DOUBLE_SLASH = auto() # //
    EQUAL = auto()        # =
    BANG = auto()         # !
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    PIPE = auto()         # |
    COMMA = auto()        # ,
    QUESTION = auto()     # ?
    POUND = auto()        # £
    STAR = auto()         # *
    AMPERSAND = auto()    # &
    AMPERSAND_COLON = auto() # &:
    HASH = auto()         # #
    AT = auto()           # @
    AT_COLON = auto()     # @:
    DOLLAR = auto()       # $
    DOLLAR_COLON = auto() # $:
    SECTION = auto()      # §
    ARROW = auto()        # =>
    DOT = auto()          # .
    PLUS = auto()         # +
    MINUS = auto()        # -
    COLON = auto()        # :
    CENT = auto()         # ¢

    # Palavras Reservadas
    AND = auto()
    OR = auto()
    NOT = auto()
    IF = auto()
    ELSE = auto()

    # Operadores de Comparação
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()

    # Literais
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    TRUE = auto()
    FALSE = auto()

    # Controle de Bloco
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', {self.literal}, L{self.line}:C{self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.errors = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            if self.column == 1:
                indent = 0
                while self.peek() == ' ' and not self.is_at_end():
                    self.advance()
                    indent += 1
                if self.peek() == '\n' or self.is_at_end() or self.peek() == '#':
                    self.start = self.current
                else:
                    if indent > self.indent_stack[-1]:
                        self.indent_stack.append(indent)
                        self.add_token(TokenType.INDENT)
                    elif indent < self.indent_stack[-1]:
                        while indent < self.indent_stack[-1]:
                            self.indent_stack.pop()
                            self.add_token(TokenType.DEDENT)
                self.start = self.current
            if not self.is_at_end():
                self.scan_token()
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, "", None, self.line, self.column))
        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == '/':
            if self.match(':'): self.add_token(TokenType.SLASH_COLON)
            elif self.match('+'): self.add_token(TokenType.SLASH_PLUS)
            elif self.match('/'): self.add_token(TokenType.DOUBLE_SLASH)
            else: self.add_token(TokenType.SLASH)
        elif c == '=':
            if self.match('>'): self.add_token(TokenType.ARROW)
            elif self.match('='): self.add_token(TokenType.EQUAL_EQUAL)
            else: self.add_token(TokenType.EQUAL)
        elif c == '!':
            if self.match('='): self.add_token(TokenType.BANG_EQUAL)
            else: self.add_token(TokenType.BANG)
        elif c == '>':
            if self.match('='): self.add_token(TokenType.GREATER_EQUAL)
            else: self.add_token(TokenType.GREATER)
        elif c == '<':
            if self.match('='): self.add_token(TokenType.LESS_EQUAL)
            else: self.add_token(TokenType.LESS)
        elif c == '.': self.add_token(TokenType.DOT)
        elif c == '+': self.add_token(TokenType.PLUS)
        elif c == '-': self.add_token(TokenType.MINUS)
        elif c == '*': self.add_token(TokenType.STAR)
        elif c == '&':
            if self.match(':'): self.add_token(TokenType.AMPERSAND_COLON)
            else: self.add_token(TokenType.AMPERSAND)
        elif c == '@':
            if self.match(':'): self.add_token(TokenType.AT_COLON)
            else: self.add_token(TokenType.AT)
        elif c == '$':
            if self.match(':'): self.add_token(TokenType.DOLLAR_COLON)
            else: self.add_token(TokenType.DOLLAR)
        elif c == '§': self.add_token(TokenType.SECTION)
        elif c == '|': self.add_token(TokenType.PIPE)
        elif c == ',': self.add_token(TokenType.COMMA)
        elif c == ':': self.add_token(TokenType.COLON)
        elif c == '(': self.add_token(TokenType.LPAREN)
        elif c == ')': self.add_token(TokenType.RPAREN)
        elif c == '[': self.add_token(TokenType.LBRACKET)
        elif c == ']': self.add_token(TokenType.RBRACKET)
        elif c == '?': self.add_token(TokenType.QUESTION)
        elif c == '£': self.add_token(TokenType.POUND)
        elif c == '¢': self.add_token(TokenType.CENT)
        elif c == '#': self.add_token(TokenType.HASH)
        elif c == '~':
            if self.match('~'):
                while self.peek() != '\n' and not self.is_at_end(): self.advance()
            else: self._error(f"Caractere inesperado '~'")
        elif c == ' ' or c == '\r' or c == '\t': pass
        elif c == '\n':
            self.add_token(TokenType.NEWLINE); self.line += 1; self.column = 1
        elif c == '"': self.string()
        else:
            if c.isdigit(): self.number()
            elif c.isalpha() or c == '_': self.identifier()
            else: self._error(f"Caractere inesperado '{c}'")

    def _error(self, message):
        err = {"line": self.line, "column": self.column - 1, "message": f"Erro Léxico: {message}"}
        self.errors.append(err)
        print(err["message"] + f" na linha {self.line}")

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_': self.advance()
        text = self.source[self.start:self.current]
        keywords = {
            "true": (TokenType.TRUE, True, "true"),
            "false": (TokenType.FALSE, False, "false"),
            "and": (TokenType.AND, None, "and"),
            "or": (TokenType.OR, None, "or"),
            "not": (TokenType.NOT, None, "not"),
            "if": (TokenType.IF, None, "if"),
            "else": (TokenType.ELSE, None, "else"),
            # Aliases em Português
            "verdadeiro": (TokenType.TRUE, True, "true"),
            "falso": (TokenType.FALSE, False, "false"),
            "ou": (TokenType.OR, None, "or"),
            "não": (TokenType.NOT, None, "not"),
            "se": (TokenType.IF, None, "if"),
            "senão": (TokenType.ELSE, None, "else")
        }
        if text in keywords:
            type_t, literal, normalized = keywords[text]
            self.tokens.append(Token(type_t, normalized, literal, self.line, self.column - (self.current - self.start)))
        else:
            self.add_token(TokenType.IDENTIFIER, text)

    def number(self):
        while self.peek().isdigit(): self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit(): self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def string(self):
        content = ""
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.column = 1

            char = self.advance()

            if char == '\\' and self.peek() == 'n':
                self.advance() # Consome o 'n'
                content += '\n'
            elif char == '\\' and self.peek() == '"':
                self.advance() # Consome o '"'
                content += '"'
            elif char == '\\' and self.peek() == '\\':
                self.advance() # Consome a '\'
                content += '\\'
            else:
                content += char

        if self.is_at_end():
            self._error("String não terminada")
            return

        self.advance() # Consome o fecha aspas
        self.add_token(TokenType.STRING, content)

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected: return False
        self.current += 1; self.column += 1; return True

    def peek(self) -> str: return '\0' if self.is_at_end() else self.source[self.current]
    def peek_next(self) -> str: return '\0' if self.current + 1 >= len(self.source) else self.source[self.current + 1]
    def is_at_end(self) -> bool: return self.current >= len(self.source)
    def advance(self) -> str: char = self.source[self.current]; self.current += 1; self.column += 1; return char
    def add_token(self, type: TokenType, literal: Any = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line, self.column - (self.current - self.start)))
