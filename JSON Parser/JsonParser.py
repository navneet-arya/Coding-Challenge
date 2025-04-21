#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this code, we define the JsonParser class, which is responsible for parsing JSON data
according to the JSON specification (RFC 8259).
"""

from JsonLexer import JsonLexer
from JsonToken import Token, TokenType


class JsonParser:
    """Parser for JSON that strictly follows the JSON specification."""

    def __init__(self, lexer):
        """Initialize the parser with a lexer."""
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        # Track whether we've already parsed a value at the root level
        self.has_parsed_root = False

    def error(self, message):
        """Raise a parser error with position information."""
        raise ValueError(
            f"Parser error at line {self.current_token.line}, column {self.current_token.column}: {message}")

    def eat(self, token_type):
        """
        Compare the current token type with the passed token type
        and if they match, "eat" the current token and assign the next
        token to self.current_token. Otherwise, raise an exception.
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

        According to JSON specification, a valid JSON document must contain
        exactly one top-level value, which can be an object, array, number,
        string, true, false, or null.
        """
        # Parse the value
        value = self.value()

        # Ensure there's nothing left after the value
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

        if token.type == TokenType.LEFT_BRACE:
            return self.object()
        elif token.type == TokenType.LEFT_BRACKET:
            return self.array()
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return token.value
        elif token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return token.value
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return True
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return False
        elif token.type == TokenType.NULL:
            self.eat(TokenType.NULL)
            return None
        else:
            self.error(f"Unexpected token: {token.type.name}")

    def object(self):
        """
        object
            : '{' '}'
            | '{' members '}'
            ;
        """
        result = {}
        self.eat(TokenType.LEFT_BRACE)

        # Empty object
        if self.current_token.type == TokenType.RIGHT_BRACE:
            self.eat(TokenType.RIGHT_BRACE)
            return result

        # Non-empty object
        self.members(result)

        # Check for trailing comma
        if self.current_token.type != TokenType.RIGHT_BRACE:
            self.error("Expected '}' or ',' in object")

        self.eat(TokenType.RIGHT_BRACE)

        return result

    def members(self, obj):
        """
        members
            : pair
            | pair ',' members
            ;
        """
        # Parse the first pair
        key, value = self.pair()

        # Check for duplicate keys (optional but recommended by some JSON standards)
        if key in obj:
            self.error(f"Duplicate key '{key}' in object")

        obj[key] = value

        # If there's a comma, parse more members
        if self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)

            # JSON does not allow trailing commas, so there must be another pair
            if self.current_token.type == TokenType.RIGHT_BRACE:
                self.error("Trailing comma in object")

            self.members(obj)

    def pair(self):
        """
        pair
            : string ':' value
            ;
        """
        # Ensure the key is a string
        if self.current_token.type != TokenType.STRING:
            self.error("Object key must be a string")

        key = self.current_token.value
        self.eat(TokenType.STRING)
        self.eat(TokenType.COLON)

        value = self.value()
        return key, value

    def array(self):
        """
        array
            : '[' ']'
            | '[' elements ']'
            ;
        """
        result = []

        self.eat(TokenType.LEFT_BRACKET)

        # Empty array
        if self.current_token.type == TokenType.RIGHT_BRACKET:
            self.eat(TokenType.RIGHT_BRACKET)
            return result

        # Non-empty array
        self.elements(result)

        # Check for trailing comma
        if self.current_token.type != TokenType.RIGHT_BRACKET:
            self.error("Expected ']' or ',' in array")

        self.eat(TokenType.RIGHT_BRACKET)

        return result

    def elements(self, arr):
        """
        elements
            : value
            | value ',' elements
            ;
        """
        # Parse a value and add it to the array
        arr.append(self.value())

        # If there's a comma, parse more elements
        if self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)

            # JSON does not allow trailing commas, so there must be another value
            if self.current_token.type == TokenType.RIGHT_BRACKET:
                self.error("Trailing comma in array")

            self.elements(arr)