# !/usr/bin/env python3
"""
Steps to be followed:
    1. Read the text and determine the frequency of each character occurring.
    2. Build the binary tree from the frequencies.
    3. Generate the prefix-code table from the tree.
    4. Encode the text using the code table.
    5. Encode the tree - we’ll need to include this in the output file so we can decode it.
    6. Write the encoded tree and text to an output field
"""

from argparse import ArgumentParser, ArgumentError
import os


def compress(file):
    # Read the text
    with open(file, "r", encoding="utf-8"):



def decompress(file):
    pass


def valid_path(file):
    if os.path.exists(file):
        return file
    return ArgumentError(f"Invalid file path: {file}")


def main():
    parser = ArgumentParser(description="Text file compression tool.")
    parser.add_argument("file", help="Enter the filename", type=valid_path, action="store", required=True)
    parser.add_argument("-c", "--compress", action="store_true", help="Flag to compress the file.")
    parser.add_argument("-d", "--decompress", action="store_true", help="Flag to decompress the file.")

    args = parser.parse_args()

    if args.c:
        compress(args.file)
    elif args.d:
        decompress(args.file)



if __name__ == '__main__':
    main()