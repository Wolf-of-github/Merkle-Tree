import hashlib
import json
import argparse
import os
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

    fp = './merkle.trees'
    if os.path.exists(fp):
        os.remove(fp)
    else:
        pass
    
    subprocess.run(["python3", "buildmtree.py"] + old_data + ["--output", "merkle.trees"])
    subprocess.run(["python3", "buildmtree.py"] + new_data + ["--output", "merkle.trees"])

    trees = load_merkle_tree("merkle.trees")
    
    old_tree = trees.get("tree_1")
    new_tree = trees.get("tree_2")

    target_hash = old_tree['hash']
    output = []

    def search(node):
        nonlocal output
        print(f'node name {node['name']}')
        if not node['left']: return False

        if node['hash'] == target_hash:
            return True

        if node['left']['hash'] == target_hash: 
            output.append([node['left']['hash'], node['right']['hash']])
            return True

        if search(node['left']):
            output.append(node['right']['hash'])
            return True

        return False


    if search(new_tree):
        output.append(new_tree['hash'])
        print(f'yes {output}')
    else:
        print(f'no {output}')
    
    print('Mekle trees for old and new lists saved in merkle.trees')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check Merkle tree consistency between two datasets.")
    parser.add_argument("--old", nargs='+', required=True, help="Old version of the dataset")
    parser.add_argument("--new", nargs='+', required=True, help="New version of the dataset")
    args = parser.parse_args()
    
    check_consistency(args.old, args.new)
