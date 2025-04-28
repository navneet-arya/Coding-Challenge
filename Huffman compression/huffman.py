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
import logging
import pickle
import struct
from argparse import ArgumentParser, ArgumentError
from utils import Tree
import os
    
# Config logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HuffmanCompressor:

    @staticmethod
    def compress_text(text):
        """ Compress the text file using Huffman coding."""

        # Determine the frequency of each character
        frequency = HuffmanCompressor.count_char(text)
        logging.debug(f"Character frequencies: {frequency}")

        # Build the binary tree from the frequencies
        tree = Tree(frequency)
        root = tree.build_binary_tree()
        logging.debug(f"Root of the tree: {root}")

        # print the tree in a readable format
        logging.debug(f"Printing the tree!!")
        logging.debug(tree.print_tree(root))

        # print generate the prefix code for each character
        codes = tree.get_code(root)
        logging.debug(f"Prefix codes: {codes}")

        # Encode the file
        encoded_text = ''.join(codes[each] for each in text)

        # Calculate padding to make a bit string length a multiple of 8
        padding = 8 - len(encoded_text) % 8
        if padding == 8:
            padding = 0

        # Add padding to make the bit string a multiple of 8
        encoded_text += "0" * padding

        # convert the bit string to bytes :: 1 byte = 8 bit
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            byte_array.append(int(byte, 2))

        return byte_array, root, padding


    @staticmethod
    def compress_file(input_file, output_file=None):
        """Compress a file using a Huffman coding"""
        logging.debug(f"input file name: {input_file}")
        if output_file is None:
            output_file = f"{input_file}.huff"

        try:
            with open(input_file, 'rb') as f:
                content = f.read()

            # convert bytes to string for compression if it's  a text file
            # for binary files, work directly with bytes
            try:
                text = content.decode('utf-8')
                is_text = True
            except UnicodeError:
                text = content
                is_text = False

            # compress the content
            byte_array, root, padding = HuffmanCompressor.compress_text(text)

            # Save a compressed data along with tree and metadata
            with open(output_file, 'wb') as f:
                # save whether the original file was text or binary
                f.write(struct.pack('?', is_text))

                # save the padding value
                f.write(struct.pack('B', padding))

                #save the huffman tree using pickle
                pickle_tree = pickle.dumps(root)
                tree_size = len(pickle_tree)
                f.write(struct.pack('I', tree_size))
                f.write(pickle_tree)

                # save the compressed data
                f.write(byte_array)

            original_size = os.path.getsize(input_file)
            compressed_size = os.path.getsize(output_file)
            compression_ratio = compressed_size / original_size

            logging.info(f"File compressed successfully.")
            logging.info(f"Original size: {original_size} bytes.")
            logging.info(f"Compressed size: {compressed_size} bytes.")
            logging.info(f"Compression ratio: {compression_ratio:.2f}")

            return output_file
        except Exception as e:
            logging.error(f"Error compressing file: {e}")
            return None

    @staticmethod
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
    parser.add_argument("-o", "--output", help="Pass the output filename")
    args = parser.parse_args()

    if args.compress:
        HuffmanCompressor.compress_file(args.file, args.output)
    elif args.decompress:
        decompress(args.file)



if __name__ == '__main__':
    main()