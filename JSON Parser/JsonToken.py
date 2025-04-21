#!/usr/bin/env python3

from enum import Enum, auto


class TokenType(Enum):
    """Token types for JSON lexical analysis."""
    LEFT_BRACE = auto()  # {
    RIGHT_BRACE = auto()  # }
    LEFT_BRACKET = auto()  # [
    RIGHT_BRACKET = auto()  # ]
    COLON = auto()  # :
    COMMA = auto()  # ,
    STRING = auto()  # "..."
    NUMBER = auto()  # 123, 123.456, -123, 1.23e+10
    TRUE = auto()  # true
    FALSE = auto()  # false
    NULL = auto()  # null
    EOF = auto()  # End of file


class Token:
    """Token class for lexical analysis."""

    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f'Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})'

    def __repr__(self):
        return self.__str__()