#!/usr/bin/env python3
import sys
import json
from hashlib import sha256
    
#keep count of levels in the merkle tree, helps in naming nodes
h_counter = 1

#hashes leaf nodes
def hash_data(data):
    return sha256(data.encode('utf-8')).hexdigest()

#a recursive function 
def build_tree(leaves):

    #if only one data point then it is assumed to be the root node of the tree
    if len(leaves) == 1:
        return leaves[0]
    
    #contains all the parents of the nodes that are hashed together
    parents = []
    i = 0
    

    while i < len(leaves):
        
        #hash two data points together and append their hash as a parent node, provide it with a name as well
        if i + 1 < len(leaves):
            left = leaves[i]
            right = leaves[i+1]
            combined = left['hash'] + right['hash']
            parent_hash = hash_data(combined)
            global h_counter
            parent = {
                'name': f'h{h_counter}',
                'hash': parent_hash,
                'left': left,
                'right': right
            }
            h_counter += 1
            parents.append(parent)
            i += 2
        #if odd number of data points remain, then promote the data point to the upper leverl
        else:
            parents.append(leaves[i])
            i += 1
    
    #recursively build the entire tree
    return build_tree(parents)

def parse_input(arg):
    arg = arg.strip()
    if arg.startswith('[') and arg.endswith(']'):
        arg = arg[1:-1]
    return [x.strip() for x in arg.split(',') if x.strip()]

def main():
    #makes sure to accept the list of data points to the for the merkle tree
    if len(sys.argv) == 1:
        sys.exit(1)
    #throws an error if here are no data points
    data_items = parse_input(sys.argv[1])
    if not data_items:
        print("No valid data items provided.")
        sys.exit(1)
    
    #hashes the leaf nodes in this code snippet 
    leaves = []
    for i, item in enumerate(data_items):
        leaf = {
            'data': item,
            'hash': hash_data(item),
            'name': f'd{i+1}'
        }
        leaves.append(leaf)
    
    #builds the tree using the build tre recursive function 
    tree = build_tree(leaves)
    
    #dumps the tree json object in the merkle.tree file which essentially represents the merkle tree
    with open('merkle.tree', 'w') as f:
        json.dump(tree, f, indent=2)
    print("Merkle tree built and saved to merkle.tree")

if __name__ == '__main__':
    main()