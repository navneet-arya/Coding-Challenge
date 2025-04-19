# !/usr/bin/env python3
# Tokenizer for JSON Parser

from enum import Enum


class TokenType(Enum):
    """Enum for token types."""

    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    COLON = ':'
    COMMA = ','
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NULL = 'NULL'
    EOF = 'EOF'


class Token:
    """Class representing a token."""

    def __init__(self, type: TokenType, value: str = '', line: int = 1, column: int = 1):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        if self.value is not None:
            return f"{self.type.name}({self.value})"
        return f"{self.type.name}"
    