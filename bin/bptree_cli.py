#!/usr/bin/env python
"""
Command-line tool for B+ tree implementation
"""

import argparse
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from dbix.bptree.bptree import BPlusTree


def main():
    parser = argparse.ArgumentParser(description='B+ Tree Implementation')
    parser.add_argument('--index-slots', type=int, required=True, help='Number of slots in index nodes')
    parser.add_argument('--leaf-slots', type=int, required=True, help='Number of slots in leaf nodes')
    parser.add_argument('--split-direction', type=str, default='left', choices=['left', 'right'], 
                       help='Split direction when nodes are split (default: left)')
    parser.add_argument('--elements', nargs='+', type=int, required=True, help='Elements to insert')
    parser.add_argument('--latex', action='store_true', help='Output in LaTeX format')
    
    args = parser.parse_args()
    
    # Create B+ tree with specified slots
    tree = BPlusTree(args.index_slots, args.leaf_slots, args.split_direction)
    
    if args.latex:
        pass
    else:
        print("Inserting elements in order:", args.elements)
    
    # Insert all elements
    for element in args.elements:
        if tree.will_cause_split(element):
            if args.latex:
                # Print the current state in LaTeX format before split
                tree.print_tree(mode="latex")
                print("\\hrule")
                print()
            else:
                print(f"Inserting {element} will cause a split")
                tree.print_tree()
                print()
        
        tree.insert(element)
        
    # Print final state only
    if args.latex:
        # Print the final tree structure in LaTeX format
        tree.print_tree(mode="latex")
    else:
        print("Final tree state:")
        tree.print_tree()


if __name__ == "__main__":
    main()