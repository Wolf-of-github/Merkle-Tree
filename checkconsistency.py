#!/usr/bin/env python3
import sys
import json
import hashlib
import argparse
import math

def hash_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_tree(leaves):
    # Recursively build the Merkle tree.
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
            # Promote the odd element to the next level.
            parents.append(leaves[i])
            i += 1
    return build_tree(parents)

def parse_input(arg):
    # Expects a list in the form "[alice, bob, carlol, david]"
    arg = arg.strip()
    if arg.startswith('[') and arg.endswith(']'):
        arg = arg[1:-1]
    return [x.strip() for x in arg.split(',') if x.strip()]

def largest_power_of_two(n):
    # For n > 1, returns the largest power of two strictly less than n.
    if n < 2:
        return 0
    p = 1 << (n.bit_length() - 1)
    if p == n:
        return p // 2
    return p

def compute_consistency_proof(m, leaf_nodes):
    """
    Compute the consistency proof between an old tree of m leaves and a new tree
    built from leaf_nodes (of total n leaves), where m <= n. The proof is computed
    recursively per RFC6962 Section 2.1.2.
    """
    n = len(leaf_nodes)
    if m == n:
        return []
    k = largest_power_of_two(n)
    if m <= k:
        proof_left = compute_consistency_proof(m, leaf_nodes[:k]) if m != k else []
        right_tree = build_tree(leaf_nodes[k:])
        return proof_left + [right_tree['hash']]
    else:
        proof_right = compute_consistency_proof(m - k, leaf_nodes[k:]) if (m - k) != (n - k) else []
        left_tree = build_tree(leaf_nodes[:k])
        return proof_right + [left_tree['hash']]

def main():
    parser = argparse.ArgumentParser(description="Check consistency between two Merkle trees.")
    parser.add_argument("old_data", help="List for the old tree (e.g., \"[alice, bob, carlol, david]\")")
    parser.add_argument("new_data", help="List for the new tree (e.g., \"[alice, bob, carlol, david, eve, fred]\")")
    args = parser.parse_args()

    old_list = parse_input(args.old_data)
    new_list = parse_input(args.new_data)
    
    # Verify that the old list is a prefix of the new list.
    if len(old_list) > len(new_list) or old_list != new_list[:len(old_list)]:
        print("no")
        # Generate trees even if inconsistent.
        old_leaves = [{'data': item, 'hash': hash_data(item)} for item in old_list]
        new_leaves = [{'data': item, 'hash': hash_data(item)} for item in new_list]
        old_tree = build_tree(old_leaves) if old_leaves else {}
        new_tree = build_tree(new_leaves) if new_leaves else {}
        trees = {"old_tree": old_tree, "new_tree": new_tree}
        with open("merkle.trees", "w") as f:
            json.dump(trees, f, indent=2)
        sys.exit(0)
    
    # Build leaf nodes for both trees.
    old_leaves = [{'data': item, 'hash': hash_data(item)} for item in old_list]
    new_leaves = [{'data': item, 'hash': hash_data(item)} for item in new_list]
    old_tree = build_tree(old_leaves) if old_leaves else {}
    new_tree = build_tree(new_leaves) if new_leaves else {}

    # Compute consistency proof for old tree size m and new tree size n.
    m = len(old_leaves)
    proof = compute_consistency_proof(m, new_leaves)

    # Write both trees to an output file.
    trees = {"old_tree": old_tree, "new_tree": new_tree}
    with open("merkle.trees", "w") as f:
        json.dump(trees, f, indent=2)

    print(f"yes {proof}")

if __name__ == '__main__':
    main()