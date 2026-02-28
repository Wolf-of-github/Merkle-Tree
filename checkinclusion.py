#!/usr/bin/env python3
import hashlib
import json
import argparse
import sys

class MerkleInclusion:
    def __init__(self, tree_file):
        self.tree = self.load_tree(tree_file)

    def load_tree(self, tree_file):
        try:
            with open(tree_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: Merkle tree file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in Merkle tree file.")
            sys.exit(1)

    def hash_string(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def find_proof(self, node, target_hash):
        # If the node is a leaf (i.e., has no children), check if it matches the target hash.
        if 'left' not in node and 'right' not in node:
            if node["hash"] == target_hash:
                return []  # Found the target leaf; no sibling hash needed at this level.
            else:
                return None

        # Search the left subtree.
        left_proof = self.find_proof(node["left"], target_hash)
        if left_proof is not None:
            # Target found in left subtree; include right sibling's name if available.
            if "right" in node and node["right"] is not None:
                return left_proof + [node["right"]["name"]]
            else:
                return left_proof

        # Search the right subtree.
        right_proof = self.find_proof(node["right"], target_hash)
        if right_proof is not None:
            # Target found in right subtree; include left sibling's name if available.
            if "left" in node and node["left"] is not None:
                return right_proof + [node["left"]["name"]]
            else:
                return right_proof

        return None

    def check_inclusion(self, data):
        target_hash = self.hash_string(data)
        proof = self.find_proof(self.tree, target_hash)
        if proof is not None:
            print(f"yes {proof}")
        else:
            print("no")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check if a string exists in the Merkle tree.")
    parser.add_argument("data", help="String to check for inclusion")
    args = parser.parse_args()

    checker = MerkleInclusion("merkle.tree")
    checker.check_inclusion(args.data)