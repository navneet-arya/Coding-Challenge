#!/usr/bin/env python3

"""
Build Your Own JSON Parser
JsonValidator.py - A simple JSON parser built from scratch that strictly adheres to the JSON specification.

Returns:
    0: Valid JSON
    1: Invalid JSON syntax
    2: File not found or permission error
    3: Input/output error
    4: Command line argument error
"""

import sys
import argparse
from enum import IntEnum
from JsonLexer import JsonLexer
from JsonParser import JsonParser


class JSONError(IntEnum):
    """Error codes for the JSON validator."""
    SUCCESS = 0
    ERROR_SYNTAX = 1
    ERROR_FILE = 2
    ERROR_IO = 3
    ERROR_ARGS = 4


def validate_json(input_text: str) -> tuple[bool, None] | tuple[bool, str]:
    """
    Validate the JSON data according to the JSON specification (RFC 8259).

    Args:
        input_text: The JSON string to validate

    Returns:
        A tuple with (is_valid, error_message)
    """
    try:
        lexer = JsonLexer(input_text)
        parser = JsonParser(lexer)
        parser.parse()
        return True, None
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def main():
    """Main function to validate JSON files."""

    parser = argparse.ArgumentParser(description="Validate JSON data from a file or stdin according to RFC 8259.")
    parser.add_argument('file', nargs='?', help='File to validate (default: stdin)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed error messages')
    parser.add_argument('-q', '--quiet', action='store_true', help="Don't print anything on success/fail")
    parser.add_argument('-p', '--pretty', action='store_true', help='Pretty print the JSON if valid')
    args = parser.parse_args()

    # Check for conflicting arguments
    if args.quiet and args.verbose:
        print("Error: Cannot use both --quiet and --verbose options together", file=sys.stderr)
        return JSONError.ERROR_ARGS

    try:
        # Read from the file or stdin
        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except FileNotFoundError:
                if not args.quiet:
                    print(f"Error: File not found: {args.file}", file=sys.stderr)
                return JSONError.ERROR_FILE
            except PermissionError:
                if not args.quiet:
                    print(f"Error: Permission denied: {args.file}", file=sys.stderr)
                return JSONError.ERROR_FILE
            except UnicodeDecodeError:
                if not args.quiet:
                    print(f"Error: File is not valid UTF-8: {args.file}", file=sys.stderr)
                return JSONError.ERROR_IO
        else:
            try:
                input_text = sys.stdin.read()
            except EOFError:
                if not args.quiet:
                    print("Error: No input provided", file=sys.stderr)
                return JSONError.ERROR_IO
            except KeyboardInterrupt:
                if not args.quiet:
                    print("\nError: Process interrupted", file=sys.stderr)
                return JSONError.ERROR_IO

        # Validate the JSON
        is_valid, error_message = validate_json(input_text)
        if is_valid:
            if not args.quiet:
                if args.pretty:
                    # Pretty print the JSON
                    try:
                        import json
                        parsed = json.loads(input_text)
                        print(json.dumps(parsed, indent=2, ensure_ascii=False))
                    except Exception as e:
                        print(f"Error while pretty printing: {e}", file=sys.stderr)
                        return JSONError.ERROR_IO
                else:
                    print("JSON is valid.")
            return JSONError.SUCCESS
        else:
            if not args.quiet:
                print(f"Invalid JSON: {error_message}", file=sys.stderr)
            return JSONError.ERROR_SYNTAX
    except Exception as e:
        if not args.quiet:
            print(f"Error: {e}", file=sys.stderr)
        return JSONError.ERROR_IO


if __name__ == '__main__':
    sys.exit(main())