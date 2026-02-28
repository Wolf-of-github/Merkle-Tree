# Merkle Tree Toolkit 

A small command-line project implementing core Merkle tree functionality in Python, including tree construction, inclusion proofs, and consistency proofs. 

## Overview

This project demonstrates how Merkle trees provide data integrity, efficient membership verification, and append-only guarantees. The implementation includes three main components: building a Merkle tree from input data, verifying whether a specific element exists in the tree using an inclusion proof, and generating consistency proofs to confirm that a new tree is an append-only extension of an older tree (as described in RFC 6962).

## Project Structure

- buildmtree.py  
- checkinclusion.py  
- checkconsistency.py  
- README.md  

## 1. Merkle Tree Construction (buildmtree.py)

Usage: `python3 buildmtree.py "[alice, bob, carol, david]"`

The program parses the command-line input, removes extra whitespace, and extracts individual data elements. Each element is hashed using SHA-256 to create leaf nodes. The tree is built recursively by pairing adjacent nodes, concatenating their hash values, and hashing the result to create parent nodes. If an odd node remains unpaired, it is promoted to the next level. This process continues until a single root node remains. The final Merkle tree is stored in JSON format in a file named `merkle.tree`. Each node contains a hash value, a unique name (e.g., d1, h1), and references to left and right children where applicable.

## 2. Inclusion Proof (checkinclusion.py)

Usage: `python3 checkinclusion.py "alice"`

This program checks whether a specific data element exists in a previously generated Merkle tree. It loads the `merkle.tree` file, hashes the input element using SHA-256, and recursively traverses the tree to find a matching leaf. If the element is found, the program prints `yes` followed by a minimal proof consisting of sibling node names required to reconstruct the Merkle root. If the element is not present, it prints `no`. The proof enables independent verification of membership by recomputing the root hash.

## 3. Consistency Proof (checkconsistency.py)

Usage: `python3 checkconsistency.py "[alice, bob, carol]" "[alice, bob, carol, david]"`

This program verifies that a new Merkle tree is an append-only extension of an older tree. It constructs Merkle trees for both input lists and checks whether the old list is a prefix of the new list. If not, it prints `no`. If it is a prefix, the program computes a consistency proof recursively by partitioning the tree at the largest power of two less than the total number of leaves. The proof consists of a minimal list of intermediate hashes that allow reconstruction of both the old and new root hashes. If consistent, the program prints `yes` followed by the proof hashes.

## Concepts Demonstrated

- SHA-256 hashing  
- Recursive tree construction  
- Hash concatenation and parent computation  
- Inclusion (membership) proofs  
- Consistency proofs (RFC 6962-style)  
- Append-only log verification  

## Author

Ishaan Apte  
MS Computer Science  
University of Southern California  
