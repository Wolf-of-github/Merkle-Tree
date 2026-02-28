# Merkle Tree Toolkit (Programming Assignment 2)

A small command-line project implementing core Merkle tree operations in Python:

- Merkle tree construction  
- Inclusion proofs  
- Consistency proofs (RFC 6962-style)  

This project demonstrates how hash-based trees provide integrity, membership verification, and append-only guarantees.

---

## Files

### 1. `buildmtree.py`

Builds a Merkle tree from a list of input data points (leaf nodes).

#### Usage

```bash
python3 buildmtree.py "[alice, bob, carol, david]"
