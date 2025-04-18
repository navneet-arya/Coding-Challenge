# JSON Lexer for parsing JSON files.
# This module contains the JsonLexer class, which is responsible for tokenizing JSON input.
# It breaks down the input into tokens that can be processed by a parser.


class JsonLexer:
    """Lexer for JSON parsing."""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
        self.column = 1

    