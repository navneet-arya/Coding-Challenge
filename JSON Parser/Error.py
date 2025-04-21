#!/usr/bin/env python3

from enum import IntEnum

class JSONError(IntEnum):
    """Error codes for the JSON validator."""
    SUCCESS = 0
    ERROR_SYNTAX = 1
    ERROR_FILE = 2
    ERROR_IO = 3
    ERROR_ARGS = 4