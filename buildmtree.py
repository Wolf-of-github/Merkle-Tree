import hashlib
import json
import argparse
import uuid

class BuildMerkleTree:
    def __init__(self):
        self.leaf_counter = 1
        self.internal_counter = 1

    def get_hash(self, hashes):
        if not hashes:
            raise ValueError('Missing hashes')

        # Ensure even number of hashes by duplicating last if needed
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])

        # Assign a unique label to each leaf node
        tree_nodes = []
        for hash_value in hashes:
            node_name = f"d{self.leaf_counter}"
            self.leaf_counter += 1
            tree_nodes.append({"hash": hash_value, "name": node_name, "left": None, "right": None, "is_leaf": True})

        # Build the tree iteratively from leaf nodes
        while len(tree_nodes) > 1:
            new_tree_nodes = []
            for i in range(0, len(tree_nodes), 2):
                left_node = tree_nodes[i]
                right_node = tree_nodes[i + 1] if i + 1 < len(tree_nodes) else left_node  # Handle odd case

                hashed = hashlib.sha256()
                hashed.update((left_node["hash"] + right_node["hash"]).encode())
                parent_hash = hashed.hexdigest()

                node_name = f"h{self.internal_counter}"
                self.internal_counter += 1

                node = {
                    "hash": parent_hash,
                    "name": node_name,
                    "left": left_node,
                    "right": right_node,
                    "is_leaf": False
                }
                new_tree_nodes.append(node)

            tree_nodes = new_tree_nodes  # Move up the tree level

        return tree_nodes[0]  # Final root node

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a Merkle tree from plain English data.")
    parser.add_argument("data", nargs="*", help="List of input text (if empty, random text will be used)")
    parser.add_argument("--output", default="merkle.tree", help="Output file name for the Merkle tree")

    args = parser.parse_args()
    
    if args.data:
        hashes = [hashlib.sha256(text.encode()).hexdigest() for text in args.data]
    else:
        hashes = [hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest() for _ in range(4)]

    m = BuildMerkleTree()
    tree = m.get_hash(hashes)

    if args.output == "merkle.trees":
        try:
            with open(args.output, "r") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        tree_key = f"tree_{len(existing_data) + 1}"
        existing_data[tree_key] = tree

        with open(args.output, "w") as f:
            json.dump(existing_data, f, indent=4)
    else:
        with open(args.output, "w") as f:
            json.dump(tree, f, indent=4)

    print("Fully structured Merkle tree with labeled nodes saved to merkle.tree")