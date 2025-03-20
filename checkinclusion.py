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
        return hashlib.sha256(data.encode()).hexdigest()

    def find_proof(self, node, target_hash, proof=[]):
        if node is None:
            return None

        if node["hash"] == target_hash:
            return proof 

        if node["left"]:
            left_proof = self.find_proof(node["left"], target_hash, proof + [node["right"]["name"]] if node["right"] else proof)
            if left_proof is not None:
                return sorted(left_proof, key=lambda x: (x[0] != 'd', x))  # Sort: dX before hX

        if node["right"]:
            right_proof = self.find_proof(node["right"], target_hash, proof + [node["left"]["name"]] if node["left"] else proof)
            if right_proof is not None:
                return sorted(right_proof, key=lambda x: (x[0] != 'd', x))  # Sort: dX before hX

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
