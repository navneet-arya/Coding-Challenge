# !/usr/bin/env python3

"""
Utility to support the huffman operations
"""
import heapq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Node:
    def __init__(self, value=0, char='', left=None, right=None):
        self.value = value
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"Node(value={self.value}, char='{self.char}', left={self.left}, right={self.right})"


class Tree:
    def __init__(self, frequency):
        """
        Initialize the tree with the character frequencies.
        :param frequency: A dictionary with characters as keys and their frequencies as values.
        """
        self.heap = [Node(value=freq, char=char) for char, freq in frequency.items()]
        heapq.heapify(self.heap)
        logging.debug(f"Initial heap created with {len(self.heap)} nodes")

    def __len__(self):
        """Return the number of nodes in the heap."""
        return len(self.heap)

    def build_binary_tree(self):
        """Build a binary tree from the character frequencies."""
        logging.info("Starting to build the binary tree.")

        if not self.heap:
            raise ValueError("Heap is empty, no tree can be built.")
        
        if len(self.heap) == 1:
            node = self.heap[0]
            return node
        
        while len(self.heap) > 1:
            # Get the two node with the lowest frequency
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)

            merged = Node(
                value = left.value + right.value,
                char = '',  # No character for internal nodes
                left = left,
                right = right
            )

            logging.debug(f"Merged node created with value: {merged.value}")
            # Add the merged node back to the heap
            heapq.heappush(self.heap, merged)
            
        # Return the root of the tree
        logging.info("Binary tree built successfully.")
        return self.heap[0]
            

    
    def get_code(self, node, code='', codes=None):
        """Generate the prefix code for each character."""
        if codes is None:
            codes = {}
        
        # base case: if the node is a leaf, assign the code
        if node.char:
            codes[node.char] = code
            logging.debug(f"Code for character '{node.char}': {code}")
            return codes

        if node.left:
            self.get_code(node.left, code+ '0', codes)
        if node.right:
            self.get_code(node.right, code + '1', codes)
        
        return codes



    def print_tree(self, node, prefix=''):
        """Print the tree in a readable format."""
        if node is None:
            return
            
        # Print current node
        if node.char:
            logging.debug(f"{prefix}Leaf: '{node.char}', Frequency: {node.value}")
        else:
            logging.debug(f"{prefix}Internal Node, Frequency: {node.value}")
            
        # Print children
        if node.left:
            self.print_tree(node.left, prefix + '  ')
        if node.right:
            self.print_tree(node.right, prefix + '  ')
