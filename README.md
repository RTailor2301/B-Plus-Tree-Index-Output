# B-Plus-Tree-Index-Output
- Takes a table file and outputs the data into a file using a B+ tree index
- Uses template code from B+ Tree in Python - Geeks for Geeks to build the tree

# How to use:
- In the main of bplustree.py, adjust the order value of the desired tree
- Change the value of the input file name in the same directory
- Change the values in the build_from_tbl function call params array to match the corresponding columns to index on
- Index will be output in "index.txt" where each row has the byte offset of the file, acting as pointer access
