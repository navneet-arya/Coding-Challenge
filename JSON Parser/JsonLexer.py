#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Lexer for parsing JSON files.
This module contains the JsonLexer class, which is responsible for tokenizing JSON input.
It breaks down the input into tokens that can be processed by a parser.
This version strictly adheres to the JSON specification (RFC 8259).
"""

from JsonToken import Token, TokenType


class JsonLexer:
    """Lexer for JSON parsing that strictly follows JSON specification (RFC 8259)."""

    def __init__(self, text: str):
        """
        Initialize the lexer with the input text.

        Args:
            text: The JSON text to tokenize
        """
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text and len(self.text) > 0 else None
        self.line = 1
        self.column = 1
        self._tokens = None
        self._token_index = 0

    def __str__(self):
        """String representation of the lexer state."""
        return f"JsonLexer(position={self.pos}, line={self.line}, column={self.column})"

    def error(self, message, line, col):
        """
        Raise an error with position information.

        Args:
            message: Error message
            line: Line number where the error occurred
            col: Column number where the error occurred
        """
        raise ValueError(f"Lexer error at line {line}, column {col}: {message}")

    def advance(self):
        """Move to the next character in the input."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1

    def peek(self, n=1):
        """
        Look ahead n characters without consuming.

        Args:
            n: Number of characters to look ahead

        Returns:
            The character n positions ahead or None if out of bounds
        """
        peek_pos = self.pos + n
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        """Skip whitespace characters (space, tab, CR, LF) as per JSON spec."""
        while (self.current_char is not None and
               self.current_char in {' ', '\t', '\r', '\n'}):
            self.advance()

    def number(self):
        """
        Parse a number according to the JSON specification.

        JSON numbers must follow this format:
        -?(0|[1-9][0-9]*)(.[0-9]+)?([eE][+-]?[0-9]+)?

        Returns:
            A Token object representing the number
        """
        result = ''
        start_line = self.line
        start_col = self.column

        # Handle negative numbers
        if self.current_char == '-':
            result += self.current_char
            self.advance()
            # After minus sign, must have at least one digit
            if not self.current_char or not self.current_char.isdigit():
                self.error("Digit expected after minus sign", self.line, self.column)

        # First digit - special handling for 0
        if self.current_char == '0':
            result += self.current_char
            self.advance()

            # Ensure no leading zeros
            if self.current_char and self.current_char.isdigit():
                self.error("Leading zeros are not allowed", self.line, self.column)
        elif self.current_char and self.current_char.isdigit():
            # Parse integer part
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        else:
            self.error("Invalid number format", self.line, self.column)

        # Handle fraction part
        if self.current_char == '.':
            result += '.'
            self.advance()

            # Must have at least one digit after decimal point
            if not self.current_char or not self.current_char.isdigit():
                self.error("At least one digit required after decimal point", self.line, self.column)

            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        # Handle exponent part
        if self.current_char in ('e', 'E'):
            result += self.current_char
            self.advance()

            # Handle exponent sign
            if self.current_char in ('+', '-'):
                result += self.current_char
                self.advance()

            # Must have at least one digit in exponent
            if not self.current_char or not self.current_char.isdigit():
                self.error("At least one digit required in exponent", self.line, self.column)

            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        # Check that the number is not immediately followed by invalid characters
        if (self.current_char and self.current_char not in
                {' ', '\t', '\r', '\n', ',', ']', '}'}):
            self.error(f"Invalid character after number: '{self.current_char}'",
                       self.line, self.column)

        # Convert string to number
        try:
            if '.' in result or 'e' in result.lower():
                return Token(TokenType.NUMBER, float(result), start_line, start_col)
            else:
                return Token(TokenType.NUMBER, int(result), start_line, start_col)
        except ValueError:
            # This shouldn't happen with our parsing logic, but just in case
            self.error(f"Invalid number format: {result}", start_line, start_col)

    def string(self):
        """
        Parse a string according to the JSON specification.

        JSON strings:
        - Must be enclosed in double quotes
        - Must properly escape special characters
        - Control characters (0-31) must be escaped

        Returns:
            A Token object representing the string
        """
        result = ''
        start_line = self.line
        start_col = self.column

        # In JSON, strings must use double quotes
        if self.current_char != '"':
            self.error("Strings must use double quotes", self.line, self.column)

        # Skip the opening quotes
        self.advance()

        while self.current_char is not None and self.current_char != '"':
            # Check for unescaped control characters (not allowed in JSON)
            if ord(self.current_char) < 32:
                self.error(
                    f"Unescaped control character (ASCII {ord(self.current_char)})",
                    self.line, self.column
                )

            # Handle escape sequences
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    self.error("Unexpected end of string", self.line, self.column)

                # Valid JSON escape sequences
                if self.current_char == '"':
                    result += '"'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == '/':
                    result += '/'
                elif self.current_char == 'b':
                    result += '\b'
                elif self.current_char == 'f':
                    result += '\f'
                elif self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == 'u':
                    # Handle Unicode escape sequences
                    hex_value = ''
                    for i in range(4):
                        self.advance()
                        if (self.current_char is None or not
                        (self.current_char.isdigit() or
                         self.current_char.lower() in 'abcdef')):
                            self.error(
                                f"Invalid Unicode escape sequence (digit {i + 1})",
                                self.line, self.column
                            )
                        hex_value += self.current_char

                    try:
                        result += chr(int(hex_value, 16))
                    except ValueError:
                        self.error(
                            f"Invalid Unicode code point: \\u{hex_value}",
                            self.line, self.column
                        )
                else:
                    self.error(
                        f"Invalid escape sequence: \\{self.current_char}",
                        self.line, self.column
                    )
            else:
                result += self.current_char

            self.advance()

        # Ensure string is properly terminated
        if self.current_char is None:
            self.error("Unterminated string", start_line, start_col)

        # Skip the closing quotes
        self.advance()
        return Token(TokenType.STRING, result, start_line, start_col)

    def _match_literal(self, expected, token_type):
        """
        Match a literal in the JSON input (true, false, null).

        Args:
            expected: The expected literal string
            token_type: The token type to return if matched

        Returns:
            A Token object of the appropriate type if matched
        """
        start_line = self.line
        start_col = self.column

        # Check if there's enough characters left
        if self.pos + len(expected) - 1 >= len(self.text):
            self.error(f"Expected '{expected}'", self.line, self.column)

        # Check for the literal
        for char in expected:
            if self.current_char != char:
                self.error(f"Expected '{expected}'", self.line, self.column)
            self.advance()

        # Ensure the literal is not followed by alphanumeric or underscore
        if (self.current_char and
                (self.current_char.isalnum() or self.current_char == '_')):
            self.error(
                f"Invalid token: '{expected}{self.current_char}'",
                self.line, self.column
            )

        # Create appropriate value based on token type
        value = None
        if token_type == TokenType.TRUE:
            value = True
        elif token_type == TokenType.FALSE:
            value = False

        return Token(token_type, value, start_line, start_col)

    def tokenize(self):
        """
        Primary method: Tokenize the entire input and return all tokens.

        This is the core lexical analysis function. It processes the entire input text
        and converts it into a sequence of tokens that can be used by a parser.

        Returns:
            A list of all tokens in the input
        """
        # Reset lexer state
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos] if self.text and len(self.text) > 0 else None
        self._token_index = 0

        tokens = []

        while self.current_char is not None:
            # Skip whitespace - only space, tab, CR, LF allowed in JSON
            if self.current_char in {' ', '\t', '\r', '\n'}:
                self.skip_whitespace()
                continue

            # Handle structural characters
            if self.current_char == '{':
                col = self.column
                self.advance()
                tokens.append(Token(TokenType.LEFT_BRACE, '{', self.line, col))
                continue

            if self.current_char == '}':
                col = self.column
                self.advance()
                tokens.append(Token(TokenType.RIGHT_BRACE, '}', self.line, col))
                continue

            if self.current_char == '[':
                col = self.column
                self.advance()
                tokens.append(Token(TokenType.LEFT_BRACKET, '[', self.line, col))
                continue

            if self.current_char == ']':
                col = self.column
                self.advance()
                tokens.append(Token(TokenType.RIGHT_BRACKET, ']', self.line, col))
                continue

            if self.current_char == ':':
                col = self.column
                self.advance()
                tokens.append(Token(TokenType.COLON, ':', self.line, col))
                continue

            if self.current_char == ',':
                col = self.column
                self.advance()
                tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                continue

            # Handle strings
            if self.current_char == '"':
                tokens.append(self.string())
                continue

            # Handle numbers
            if self.current_char == '-' or self.current_char.isdigit():
                tokens.append(self.number())
                continue

            # Handle literals true, false, null
            if self.current_char == 't':
                tokens.append(self._match_literal("true", TokenType.TRUE))
                continue

            if self.current_char == 'f':
                tokens.append(self._match_literal("false", TokenType.FALSE))
                continue

            if self.current_char == 'n':
                tokens.append(self._match_literal("null", TokenType.NULL))
                continue

            # Single quotes are common error - give helpful message
            if self.current_char == "'":
                self.error(
                    "Single quotes are not allowed in JSON. Use double quotes for strings.",
                    self.line, self.column
                )

            # Any other character is invalid in JSON
            self.error(
                f"Unexpected character: '{self.current_char}'",
                self.line, self.column
            )

        # Add EOF token
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        self._tokens = tokens
        return tokens

    def get_next_token(self):
        """
        Return the next token in the input sequence.
        This method uses tokenize() to get all tokens and then returns them one by one.

        Returns:
            The next Token object from the input
        """
        # If not tokenized yet, do it now
        if self._tokens is None:
            self.tokenize()

        # Return current token and advance index
        if self._token_index < len(self._tokens):
            token = self._tokens[self._token_index]
            self._token_index += 1
            return token
        else:
            # Return EOF token if we've gone through all tokens
            return self._tokens[-1]