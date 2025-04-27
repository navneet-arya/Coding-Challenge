# !/usr/bin/env python3

"""
Utility to support the huffman operations
"""
import heapq


class Node:
    def __init__(self, value=0, char='', left=None, right=None):
        self.value = value
        self.char = char
        self.left = left
        self.right = right

class Tree:

    def __init__(self, frequency):
        """
        :param frequency: A dictionary with characters as keys and their frequencies as values.
        """
        self.heap = [(value, key) for key, value in frequency.items()]
        heapq.heapify(self.heap)

    def build_binary_tree(self):
        """Build a binary tree from the character frequencies."""

        while self.heap:
            first, second = heapq.nsmallest(2, self.heap)


        return None
