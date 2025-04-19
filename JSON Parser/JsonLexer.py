# JSON Lexer for parsing JSON files.
# This module contains the JsonLexer class, which is responsible for tokenizing JSON input.
# It breaks down the input into tokens that can be processed by a parser.

from JsonToken import Token, TokenType


class JsonLexer:
    """Lexer for JSON parsing."""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.float = False
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
        self.column = 1

    def error(self, message, line, col):
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
    
    def skip_whitspace(self):
        """Skip Whitspace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    
    def number(self):
        """Parse a number: integer or float."""

        result = ''
        start_line = self.line
        start_col = self.column

        # Handle negative numbers
        if self.current_char == '-':
            result += self.current_char
            self.advance()

        # Handle Integer part
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Handle Decimal/decimal/floating part
        if self.current_char == '.':
            if not self.float:
                self.float = True
                result += '.'
                self.advance()

                # Must have at least one digit after decimal point
                if not (self.current_char is not None and self.current_char.isdigit()):
                    self.error("Invalid number format", self.line, self.column)
                
                while self.current_char is not None and self.current_char.isdigit():
                    result += self.current_char
                    self.advance()
            else:
                self.error("Invalid number format", self.line, self.column)

        # Handle Exponential part
        if self.current_char in ('e', 'E'):
            result += self.current_char
            self.advance()

            # Handle Exponential sign
            if self.current_char in ('+', '-'):
                result += self.current_char
                self.advance()
            
            # Must have at least one digit in exponent
            if not (self.current_char is not None and self.current_char.isdigit()):
                self.error("Invalid number format", self.line, self.column)
            
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        
        # Convert string to number
        try:
            if '.' in result or 'e' in result.lower():
                value = float(result)
            else:
                value = int(result)
            print(Token(TokenType.NUMBER, value, start_line, start_col)) 
            return Token(TokenType.NUMBER, value, start_line, start_col)
        except ValueError:
            self.error("Invalid number format", self.line, self.column)
    
    def string(self):
        """Parse a string enclosed in double/single quotes."""
        result = ''
        start_line = self.line
        start_col = self.column

        # skip the opening quotes
        self.advance()

        while self.current_char is not None and (self.current_char != '"' or self.current_char == "'"):
            # we need to handle escape sequences because JSON allows them
            # Replacing the escape sequences with their actual values
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    self.error("Unexpected end of string literal.", self.line, self.column)
                
                
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == 'b':
                    result += '\b'
                elif self.current_char == '"':
                    result += '"'
                elif self.current_char == "'":
                    result += "'"
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == '/':
                    result += '/'
                elif self.current_char == 'f':
                    result += '\f'
                elif self.current_char == 'u':
                    # Handle Unicode escape sequences
                    self.advance()
                    hex_value = ''
                    for _ in range(4):
                        if self.current_char is None or not self.current_char.isalnum():
                            self.error("Invalid unicode escape sequence", self.line, self.column)
                        hex_value += self.current_char
                        self.advance()
                    try:
                        result += chr(int(hex_value, 16))
                    except ValueError:
                        self.error("Invalid unicode escape sequence", self.line, self.column)
                else:
                    self.error("Invalid escape sequence", self.line, self.column)
            else:
                result += self.current_char
            self.advance()
        
        if self.current_char is None:
            self.error("Unexpected end of string literal", self.line, self.column)
        
        # skip the closing quotes
        self.advance()
        print(Token(TokenType.STRING, result, start_line, start_col))
        return Token(TokenType.STRING, result, start_line, start_col)


    def get_text_token(self):
        """
        Return the next token in the input.
        This method is called by the parser to get tokens one at a time.
        """
        while self.current_char is not None:
            # Skip whiteSpace
            if self.current_char.isspace():
                self.skip_whitspace()
                continue

            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LEFT_BRACE, line=self.line, column=self.column-1)

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RIGHT_BRACE, line=self.line, column=self.column-1)

            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LEFT_BRACKET, line=self.line, column=self.column-1)

            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RIGHT_BRACKET, line=self.line, column=self.column-1)

            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, line=self.line, column=self.column-1)

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, line=self.line, column=self.column-1)

            if self.current_char == '"' or self.current_char == "'":
                return self.string()

            if self.current_char.isdigit() or self.current_char == '-':
                return self.number()

            if self.current_char == 't':
                # Check for "true"
                start_column = self.column
                if (
                    self.pos + 3 < len(self.text) and
                    self.text[self.pos:self.pos+4] == "true"
                ):
                    for _ in range(4):
                        self.advance()
                    return Token(TokenType.TRUE, True, self.line, start_column)
                else:
                    self.error("Unexpected token.", self.line, self.column)

            if self.current_char == 'f':
                # Check for "false"
                start_column = self.column
                if (
                    self.pos + 3 < len(self.text) and
                    self.text[self.pos:self.pos+5] == "false"
                ):
                    for _ in range(5):
                        self.advance()
                    return Token(TokenType.FALSE, False, self.line, start_column)
                else:
                    self.error("Unexpected token.", self.line, self.column)

            if self.current_char == 'n':
                # Check for null
                start_column = self.column
                if (
                    self.pos + 3 < len(self.text) and
                    self.text[self.pos:self.pos+4] == 'null'
                ):
                    for _ in range(4):
                        self.advance()
                    return Token(TokenType.NULL, None, self.line, start_column)
                else:
                    self.error("Unexpected token", self.line, self.column)
        return Token(TokenType.EOF, line=self.line, column=self.column)
