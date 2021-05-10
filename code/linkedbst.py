"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log

from random import randrange
import time
from tqdm import tqdm


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            strr = ""
            if node != None:
                strr += recurse(node.right, level + 1)
                strr += "| " * level
                strr += str(node.data) + "\n"
                strr += recurse(node.left, level + 1)
            return strr

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        parent = None

        if self._root == None:
            self._root = BSTNode(item)
            return
        
        curr = self._root
        # Search process
        while curr:
            parent = curr
            if curr.data <= item:
                curr = curr.right
            elif curr.data > item:
                curr = curr.left
        # Append the item to the needed place
        if item < parent.data:
            parent.left = BSTNode(item)
        else:
            parent.right = BSTNode(item)

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def lift_max_in_leftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = "L"
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = "L"
                current_node = current_node.left
            else:
                direction = "R"
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None and not current_node.right == None:
            lift_max_in_leftsubtreetotop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        height = self.height()
        size = self._size

        return height < 2 * log(size + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        range_children = []
        for node in self.inorder():
            if low <= node <= high:
                range_children.append(node)

        return range_children

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        ordered = []
        for elem in self.inorder():
            ordered.append(elem)

        self.clear()

        def recurse(input_list):
            """
            Split the list recuresively
            """
            if not input_list:
                return None

            mid = len(input_list) // 2

            return BSTNode(
                input_list[mid],
                recurse(input_list[:mid]),
                recurse(input_list[mid + 1 :]),
            )

        self._root = recurse(ordered)
        self._size = len(ordered)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        succ = None
        root = self._root
        while root != None:
            if item > root.data:
                root = root.right
            elif item < root.data:
                succ = root
                root = root.left
            else:
                min_node = self.find_min(root.right)
                if not min_node:
                    if not succ:
                        return succ
                    return succ.data
                return min_node.data
        # If there in no item, the successor is the smallest one
        backup_min = self.find_min(self._root)
        if not backup_min:
            return None
        return backup_min.data

    def find_min(self, input_root):
        """
        Find min element from a certain root
        """
        root = input_root
        # Don't accept empty roots
        if not root:
            return root
        # Go left until you canr
        while root.left:
            root = root.left
        return root

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        pred = None
        root = self._root
        while root != None:
            if item > root.data:
                pred = root
                root = root.right
            elif item < root.data:
                root = root.left
            else:
                max_node = self.find_max(root.left)
                if not max_node:
                    if not pred:
                        return pred
                    return pred.data
                return max_node.data
        return None

    def find_max(self, input_root):
        """
        Find min element from a certain root
        """
        root = input_root
        # Dont accept empty roots
        if not root:
            return root
        # Go right until you can'r
        while root.right:
            root = root.right
        return root

    def demo_bst(self, path="data/words.txt"):
        """
        Check speed of element search in:
        list
        Unbalanced alphabetical order BT
        Unbalanced random order BT
        Balanced BT
        """
        words = []
        with open(path, "r") as file:
            words = file.read().split()

        # 1 Search in list
        search_list = words[:900]
        curr_time = time.time()
        for i in tqdm(range(10000), desc="Searching in list"):
            num_idx = randrange(0, len(words))
            try:
                _word = search_list.index(words[num_idx])
            except ValueError:
                _word = None
        print("List search 10000 words: ", time.time() - curr_time, " sec\n")

        # Creating an unbalanced, alphabetical order tree
        for i in words[:900]:
            self.add(i)
        # 2 Searching 10000 elem in that tree
        curr_time = time.time()
        for i in tqdm(range(10000), desc="Searching in unbalanced alphabetical order tree"):
            num_idx = randrange(0, len(words))
            self.find(words[num_idx])
        print("Unbalanced alphabetical tree(len=900) search 10000 words|", time.time() - curr_time, "|sec\n")
        # Clear the tree
        self.clear()

        # 3 Creating an unbalanced, random order tree
        for i in range(900):
            idx = randrange(0, len(words))
            self.add(words[idx])
        # Searching 10000 elem in that tree
        curr_time = time.time()
        for i in tqdm(range(10000), desc="Searching in unbalanced random order tree"):
            num_idx = randrange(0, len(words))
            self.find(words[num_idx])
        print("Unbalanced random order tree(len=900) search 10000 words|", time.time() - curr_time, "|sec\n")

        # 4 Rebalance the tree
        self.rebalance()

        # Searching 10000 elem in that tree
        curr_time = time.time()
        for i in tqdm(range(10000), desc="Searching in Balanced tree"):
            num_idx = randrange(0, len(words))
            self.find(words[num_idx])
        print("Balanced tree tree(len=900) search 10000 words|", time.time() - curr_time, "|sec\n")




if __name__ == "__main__":
    tree = LinkedBST([])
    tree.demo_bst()
   
