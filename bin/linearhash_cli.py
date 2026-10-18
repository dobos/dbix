#!/usr/bin/env python
"""
Command-line tool for linear hash table implementation
"""

import argparse
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from dbix.linearhash.linearhashtable import LinearHashTable


def main():
    parser = argparse.ArgumentParser(description='Linear Hash Table Implementation')
    parser.add_argument('--slots-per-bucket', type=int, required=True, help='Number of slots in each bucket')
    parser.add_argument('--fill-factor', type=float, required=True, help='Fill factor threshold')
    parser.add_argument('--hash-values', nargs='+', type=int, required=True, help='Hash values to insert')
    parser.add_argument('--latex', action='store_true', help='Output in LaTeX format')
    parser.add_argument('--binary', action='store_true', help='Output hash values in binary format')
    
    args = parser.parse_args()
    
    # Create linear hash table with specified parameters
    table = LinearHashTable(args.slots_per_bucket, args.fill_factor)
    
    if args.latex:
        pass
    else:
        print("Inserting hash values in order:", args.hash_values)
    
    # Insert all hash values
    for hash_value in args.hash_values:
        if table.will_cause_split():
            if args.latex:
                # Print the current state in LaTeX format before split
                table.print_hashtable("latex", binary=args.binary)
                print("\\hrule")
                print()
            else:
                print(f"Inserting {hash_value} will cause a split")
                table.print_hashtable("text", binary=args.binary)
                print()
        
        # Now actually insert the value
        table.insert(hash_value)
    
    # Print final state only
    if args.latex:
        # Print the final table structure in LaTeX format
        table.print_hashtable("latex", binary=args.binary)
    else:
        print("Final table state:")
        table.print_hashtable("text", binary=args.binary)


if __name__ == "__main__":
    main()