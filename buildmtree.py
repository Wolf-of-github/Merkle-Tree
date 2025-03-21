#!/usr/bin/env python3
import sys
import json
from hashlib import sha256

def hash_data(data):
    return sha256(data.encode('utf-8')).hexdigest()

def build_tree(leaves):
    
    if len(leaves) == 1:
        return leaves[0]
    
    parents = []
    i = 0
    
    while i < len(leaves):
        if i + 1 < len(leaves):
            left = leaves[i]
            right = leaves[i+1]
            combined = left['hash'] + right['hash']
            parent_hash = hash_data(combined)
            parent = {
                'hash': parent_hash,
                'left': left,
                'right': right
            }
            parents.append(parent)
            i += 2
        else:
           
            parents.append(leaves[i])
            i += 1
    return build_tree(parents)

def parse_input(arg):
    
    # Expecting input in the format: "[alice, bob, carlol, david]"
    arg = arg.strip()
    if arg.startswith('[') and arg.endswith(']'):
        arg = arg[1:-1]
    return [x.strip() for x in arg.split(',') if x.strip()]

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    
    data_items = parse_input(sys.argv[1])
    if not data_items:
        print("No valid data items provided.")
        sys.exit(1)
    
    # Create leaf nodes.
    leaves = []
    for item in data_items:
        leaf = {
            'data': item,
            'hash': hash_data(item)
        }
        leaves.append(leaf)
    
    tree = build_tree(leaves)
    
    with open('merkle.tree', 'w') as f:
        json.dump(tree, f, indent=2)
    print("Merkle tree built and saved to merkle.tree")

if __name__ == '__main__':
    main()