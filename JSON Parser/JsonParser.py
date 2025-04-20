# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# In this code, we define the JsonParser class, which is responsible for parsing JSON data.


from JsonLexer import JsonLexer
from token import Token, TokenType

class JsonParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        print(self.current_token)

    def error(self, message):
        raise ValueError(
            f"Parser error at line {self.current_token.line}, column {self.current_token.column}: {message}")
    
    def eat(self, token_type):
        """
        Compare the current token type with the passed token type
        and if they match, "eat" the current token and assign the next
        token to self.current_token. Otherwise, rasie an exception.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(
                f"Expected {token_type.name}, got {self.current_token.type.name}"
            )
    
    def parse(self):
        """
        Parse the JSON input and return the result.
        
        json
            : value EOF
            ;
        """
        value = self.value()
        self.eat(TokenType.EOF)
        return value
    
    def value(self):
        """
        value 
            : object
            | array
            | string
            | number
            | "true"
            | "false"
            | "null"
            ;
        """
        token = self.current_token

