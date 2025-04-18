# !/usr/bin/env python3

"""
Build Your Own JSON Parser
json_validator.py - A simple JSON parser built from scratch

Returns:
    0: Valid JSON
    1: Invalid JSON syntax
    2: File not found or permission error
    3: Input/output error
    4: Command line argument error
"""

import sys
import argparse
from Error import JSONError
from JsonLexer import JsonLexer
from JsonParser import JsonParser


def validate_json(input_text: str) -> tuple[bool, str]: 
    """ Validate the JSON data. """
    try:
        lexer = JsonLexer(input_text)
        return True, None
    except ValueError as e:
        return False, str(e)


def main():
    """ Main function to validate JSON files."""

    parser = argparse.ArgumentParser(description="Validate JSON data from a file or stdin.")
    parser.add_argument('file', nargs='?', help='File to validate (default: stdin)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed error messages')
    parser.add_argument('-q', '--quiet', action='store_true', help="Don't print anything on sucess/fail")
    parser.add_argument('-p','--pretty', action='store_true', help='Pretty print the JSON if valid')
    args = parser.parse_args()

    try:
        # Read from the file or stdin
        if args.file:
            try:
                with open(args.file, 'r') as f:
                    input_text = f.read()
            except FileNotFoundError:
                if not args.quiet:
                    print(f"Error: File not found: {args.file}", file=sys.stderr)
                return JSONError.ERROR_FILE
            except PermissionError:
                if not args.quiet:
                    print(f"Error: Permission denied: {args.file}", file=sys.stderr)
                return JSONError.ERROR_FILE
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
        
        # validate the JSON
        is_valid, error_message = validate_json(input_text)


    except Exception as e:
        if not args.quiet:
            print(f"Error: {e}", file=sys.stderr)
        return JSONError.ERROR_UNKNOWN
        



if __name__ == '__main__':
    sys.exit(main())

