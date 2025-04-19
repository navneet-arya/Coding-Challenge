# !/usr/bin/env python3


from JsonLexer import JsonLexer


class JsonParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise ValueError(
            f"Parser error at line {self.current_token.line}, column {self.current_token.column}: {message}")