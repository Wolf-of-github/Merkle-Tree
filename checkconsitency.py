import hashlib
import json
import argparse
import sys

class MerkleTree:
    def __init__(self, data):
        """Initialize the Merkle tree with a list of strings."""
        self.leaves = [self.hash_string(item) for item in data]
        self.tree = self.build_tree(self.leaves)
        self.root = self.tree[0] if self.tree else None

    def hash_string(self, data):
        """Hash a string using SHA-256."""
        return hashlib.sha256(data.encode()).hexdigest()

    def build_tree(self, leaves):
        """Construct the Merkle tree and return a list of hashes from bottom to top."""
        if not leaves:
            return []
        
        tree = leaves[:]
        while len(tree) > 1:
            if len(tree) % 2 != 0:
                tree.append(tree[-1])  # Duplicate last node if odd number
            tree = [self.hash_string(tree[i] + tree[i+1]) for i in range(0, len(tree), 2)]
        return tree

    def get_root(self):
        """Return the root hash of the Merkle tree."""
        return self.root


def check_consistency(old_data, new_data):
    """Check if the new Merkle tree is a consistent extension of the old one."""
    old_tree = MerkleTree(old_data)
    new_tree = MerkleTree(new_data)
    
    old_root = old_tree.get_root()
    new_root = new_tree.get_root()
    
    if old_root is None or new_root is None:
        print("Error: One of the trees is empty.")
        sys.exit(1)
    
    # Verify if the old tree is a subset of the new tree
    if old_data != new_data[:len(old_data)]:
        print("no")
        return
    
    # Generate a consistency proof
    proof = [old_root]
    intermediate_hashes = new_tree.tree[1:len(new_tree.tree)-1]  # Collect intermediate hashes
    proof.extend(intermediate_hashes)
    proof.append(new_root)
    
    print("yes", proof)

    # Save trees to a file for debugging
    with open("merkle.trees", "w") as f:
        json.dump({"old_tree": old_tree.tree, "new_tree": new_tree.tree}, f, indent=4)
    print("Merkle trees saved to merkle.trees")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check Merkle tree consistency between two datasets.")
    parser.add_argument("old_data", nargs='+', help="Old version of the dataset")
    parser.add_argument("new_data", nargs='+', help="New version of the dataset")
    args = parser.parse_args()
    
    check_consistency(args.old_data, args.new_data)
