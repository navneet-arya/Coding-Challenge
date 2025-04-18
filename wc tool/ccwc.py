#!/usr/bin/env python3


# Build Your Own wc Tool
# This challenge is to build your own version of the Unix command line tool wc!
# each tool can be easily connected to other tools to create incredibly powerful compositions.
# The wc command is a simple tool that counts the number of lines, words, and characters in a file or standard input.


import sys
from argparse import ArgumentParser


def count_file(file, count_lines=True, count_words=True, count_chars=True, count_bytes=False):
    """
    Count lines, words, characters and bytes in a file.
    :param file: File object to read from.
    :param count_lines: Boolean to count lines.
    :param count_words: Boolean to count words.
    :param count_chars: Boolean to count characters.
    :param count_bytes: Boolean to count bytes.
    :return: Tuple of counts (lines, words, chars).
    """

    line_count = word_count = char_count = 0

    for line in file:
        if count_lines: line_count += 1
        if count_words: word_count += len(line.split())
        if count_chars or count_bytes: char_count += len(line)

    return line_count, word_count, char_count


def print_results(lines, words, chars, show_lines, show_words, show_chars, show_bytes, filename):
    """Print count results in the same format as the Unix wc command."""
    output = ""
    if show_lines:
        output += f"{lines:8}"
    if show_words:
        output += f"{words:8}"
    if show_chars:
        output += f"{chars:8}"
    if show_bytes and not show_chars:
        output += f"{chars:8}"
    
    if filename:
        output += f" {filename}"
    
    print(output)


def argument_parser():
    parser = ArgumentParser(description='Count lines, words and characters in a file.')
    parser.add_argument('files', nargs='*', help='Files to count. If no files are specified, stdin is used.')
    parser.add_argument('-l', '--lines', action='store_true', help='Print the lines count.')
    parser.add_argument('-w', '--words', action='store_true', help='Print the words count.')
    parser.add_argument('-c', '--chars', action='store_true', help='Print the characters count.')
    parser.add_argument('-m', '--bytes', action='store_true', help='Print the byte count (same as -c in this implementation)')

    return parser.parse_args()

def main():
    args = argument_parser()
    total_lines, total_words, total_chars = 0, 0, 0

    # If no options are specified, count everything
    if not (args.lines or args.words or args.chars or args.bytes):
        args.lines = args.words = args.chars = args.bytes = True
    
    # If no files are specified, use stdin
    if not args.files:
        lines, words, chars = count_file(sys.stdin, args.lines, args.words, args.chars or args.bytes)
        print_results(lines, words, chars, args.lines, args.words, args.chars, args.bytes, "")
    
    else:
        # check if the files exist
        for filename in args.files:
            try:
                with open(filename, 'r', encoding="utf8") as file:
                    lines, words, chars = count_file(file, args.lines, args.words, args.chars or args.bytes)
                    print_results(lines, words, chars, args.lines, args.words, args.chars, args.bytes, filename)

            except IOError as e:
                print(f"wc.py: {filename}: {e.strerror}", file=sys.stderr)
        
        # Print totals if more than one file was processed
        if len(args.files) > 1:
            print_results(total_lines, total_words, total_chars, args.lines, args.words, args.chars, args.bytes, "total")


if __name__ == '__main__':
    main()