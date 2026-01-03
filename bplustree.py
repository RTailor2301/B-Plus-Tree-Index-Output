"""
HOW TO USE:
In the __main__, adjust the value of the order and how the index will be built
The file name of the table should replace "example.tbl" in the main
The column indices correspond to the index of each column and should be replaced accordingly
in the array in the build_from_tbl function call
"""

import math

class Node:
    def __init__(self, order):
        self.order = order
        self.max_keys = order
        self.max_children = order + 1
        self.min_keys = int(math.ceil(order / 2.0))
        self.min_children = self.min_keys + 1
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.check_leaf = False

    # Insert at the leaf
    def insert_at_leaf(self, leaf, value, key):
        if (self.values):
            temp1 = self.values
            for i in range(len(temp1)):
                if (value == temp1[i]):
                    self.keys[i].append(key)
                    break
                elif (value < temp1[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(temp1)):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]

class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True

    def insert(self, value, key):
        # value for string comparison -- removed
        # value = str(value)
        old_node = self.search(value)
        old_node.insert_at_leaf(old_node, value, key)

        if (len(old_node.values) > old_node.max_keys):
            node1 = Node(old_node.order)
            node1.check_leaf = True
            node1.parent = old_node.parent
            total = len(old_node.values)
            left_count = int(math.ceil((total) / 2.0))
            node1.values = old_node.values[left_count:]
            node1.keys = old_node.keys[left_count:]
            node1.nextKey = old_node.nextKey
            old_node.values = old_node.values[:left_count]
            old_node.keys = old_node.keys[:left_count]
            old_node.nextKey = node1
            promote_key = node1.values[0]
            self.insert_in_parent(old_node, promote_key, node1)

    # Search operation
    def search(self, value):
        current_node = self.root
        while(current_node.check_leaf == False):
            temp2 = current_node.values
            for i in range(len(temp2)):
                if (value == temp2[i]):
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < temp2[i]):
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    # Find
    def find(self, value, key):
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False

    # Insert in parent
    def insert_in_parent(self, n, value, ndash):
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.check_leaf = False
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp3 = parentNode.keys
        for i in range(len(temp3)):
            if (temp3[i] == n):
                parentNode.values = parentNode.values[:i] + \
                    [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i +
                                                1] + [ndash] + parentNode.keys[i + 1:]
                if len(parentNode.values) > parentNode.max_keys:
                    parentdash = Node(parentNode.order)
                    parentdash.check_leaf = False
                    parentdash.parent = parentNode.parent

                    mid = len(parentNode.values) // 2
                    promote_value = parentNode.values[mid]

                    parentdash.values = parentNode.values[mid+1:]
                    parentdash.keys = parentNode.keys[mid+1:]

                    parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid+1]

                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash

                    self.insert_in_parent(parentNode, promote_value, parentdash)

#####################################################################################

def printTree(tree):
    q = [(tree.root, 0)]
    current_level = 0
    print("LEVEL 0:")

    while q:
        node, level = q.pop(0)

        if level != current_level:
            current_level = level
            print(f"\nLEVEL {level}:")

        print(node.values, "(leaf)" if node.check_leaf else "")

        if not node.check_leaf:
            for child in node.keys:
                q.append((child, level + 1))


# count total nodes (bfs)
def count_nodes(root):
    q = [root]
    count = 0
    while q:
        n = q.pop(0)
        count += 1
        if not n.check_leaf:
            q.extend(n.keys)
    return count


def tree_height(root):
    h = 0
    node = root
    while node and not node.check_leaf:
        node = node.keys[0]
        h += 1
    return h + 1 # count leaf level

def build_from_tbl(filename, tree, columns):
    with open(filename, "r") as f:
        while True:
            row_pos = f.tell()    
            line = f.readline()     

            if not line:
                break

            line = line.strip()
            if not line:
                continue

            cols = line.split("|")

            # build key
            key_vals = [convert_if_numeric(cols[c]) for c in columns]
            bpt_key = key_vals[0] if len(key_vals) == 1 else tuple(key_vals)

            # row is pointer to record using offset
            tree.insert(bpt_key, row_pos)

def write_index(tree, outname="index.txt"):
    node = tree.root
    while not node.check_leaf:
        node = node.keys[0]

    with open(outname, "w") as out:
        while node:
            for i, v in enumerate(node.values):
                # v can have multiple record pointers
                for rec_ptr in node.keys[i]:
                    out.write(f"{v} -> {rec_ptr}\n")
            node = node.nextKey


def convert_if_numeric(s):
    if s.isdigit():
        return int(s)
    try:
        return float(s) 
    except ValueError:
        return s 

if __name__ == "__main__":
    order = 3
    bpt = BplusTree(order)

    build_from_tbl("example.tbl", bpt, [0])

    printTree(bpt)
    print("Height:", tree_height(bpt.root))
    print("Total nodes:", count_nodes(bpt.root))

    write_index(bpt, "index.txt")
