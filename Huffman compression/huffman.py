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
from utils import Tree
import os
    

def count_char(text):
    """
    Count the frequency of each character in the text.
    :param text: The input text to be compressed.
    :return: A dictionary with characters as keys and their frequencies as values.
    """
    count = {}
    for char in text:
        if char in count:
            count[char] += 1
        else:
            count[char] = 1
    return count


def compress(file):
    """ Compress the text file using Huffman coding."""

    # Read the text
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Determine the frequency of each character
    frequency = count_char(text)
    print(f"Character frequencies: {frequency}")

    # Build the binary tree from the frequencies
    Tree.build_binary_tree(frequency)




def decompress(file):
    pass


def valid_path(file):
    """ Validate the file path."""
    
    if os.path.exists(file):
        return file
    return ArgumentError(f"Invalid file path: {file}")


def main():
    """ Main function to handle command line arguments and call the appropriate functions."""

    # Create the argument parser
    parser = ArgumentParser(description="Text file compression tool.")
    parser.add_argument("file", help="Enter the filename", type=valid_path, action="store")
    parser.add_argument("-c", "--compress", action="store_true", help="Flag to compress the file.", default=True)
    parser.add_argument("-d", "--decompress", action="store_true", help="Flag to decompress the file.")

    args = parser.parse_args()

    if args.compress:
        compress(args.file)
    elif args.decompress:
        decompress(args.file)



if __name__ == '__main__':
    main()