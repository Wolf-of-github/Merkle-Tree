import hashlib
import json
import argparse
import sys
import subprocess

def load_merkle_tree(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not load {file_path}")
        sys.exit(1)

def check_consistency(old_data, new_data):
    
    # Call buildmtree.py to generate trees
    subprocess.run(["python3", "buildmtree.py"] + old_data + ["--output", "merkle.trees"])
    subprocess.run(["python3", "buildmtree.py"] + new_data + ["--output", "merkle.trees"])

    trees = load_merkle_tree("merkle.trees")
    
    old_tree = trees.get("tree_1")
    new_tree = trees.get("tree_2")

    if not old_tree or not new_tree:
        print("Error: Merkle trees were not generated correctly.")
        sys.exit(1)

    old_root = old_tree["hash"]
    new_root = new_tree["hash"]

    if old_data != new_data[:len(old_data)]:
        print("no")
        return

    proof = [old_root]
    proof.append(new_root)

    print("yes", proof)
    print("Merkle trees saved to merkle.trees")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check Merkle tree consistency between two datasets.")
    parser.add_argument("--old", nargs='+', required=True, help="Old version of the dataset")
    parser.add_argument("--new", nargs='+', required=True, help="New version of the dataset")
    args = parser.parse_args()
    
    check_consistency(args.old, args.new)
