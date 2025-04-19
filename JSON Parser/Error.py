# !/user/bin/env python3
# -*- coding: utf-8 -*-

""" Contain all the information about the error that can be raised by the parser."""

class JSONError(Exception):
    """Base class for all the JSON errors."""
    ERROR_SYNTAX = 1
    ERROR_FILE = 2
    ERROR_IO = 3
    ERROR_ARGUMENT = 4
    ERROR_UNKNOWN = 5

    def error(message, line, col):
        raise ValueError(f"Lexer error at line {line}, column {col}: {message}")