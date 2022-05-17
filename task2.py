# pylint: disable=invalid-name
"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log
import random
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


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
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

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
        node = self._root
        while True:
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def adddd(node):
            # New item is less, go left until spot is found
            while True:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right is None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            adddd(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None
        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode is None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved is None:
            return None
        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        counter1 = 0
        stack = LinkedStack([self._root])
        if self._root is None:
            return None
        while not stack.isEmpty():
            elements = []
            while not stack.isEmpty():
                elements.append(stack.pop())
            for elem in elements:
                if elem.left is not None:
                    stack.push(elem.left)
                if elem.right is not None:
                    stack.push(elem.right)
            counter1 += 1
        return counter1 - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        counter1 = 0
        stack = LinkedStack([self._root])
        if self._root is None:
            return None
        while not stack.isEmpty():
            elem = stack.pop()
            counter1 += 1
            if elem.left is not None:
                stack.push(elem.left)
            if elem.right is not None:
                stack.push(elem.right)

        if self.height() < 2 * log(counter1 + 1) / log(2) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = []
        stack = LinkedStack([self._root])
        while not stack.isEmpty():
            elem = stack.pop()
            if elem is None:
                continue
            if low <= elem.data <= high:
                stack.push(elem.left)
                stack.push(elem.right)
                res.append(elem.data)
            elif high < elem.data:
                stack.push(elem.left)
            else:
                stack.push(elem.right)
        return sorted(res)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        elem_list = []
        stack = LinkedStack([self._root])
        while not stack.isEmpty():
            elem = stack.pop()
            elem_list.append(elem.data)
            if elem.left is not None:
                stack.push(elem.left)
            if elem.right is not None:
                stack.push(elem.right)

        self._size = 0
        self._root = None
        elem_list.sort()

        check_list = [(0, len(elem_list))]
        while elem_list != len(elem_list) * ['checked']:
            new_check_list = []
            for i in check_list:
                pos = (i[0] + i[1]) // 2
                if i[0] == i[1] or elem_list[pos] == 'checked':
                    continue
                new_check_list.append((i[0], pos))
                new_check_list.append((pos + 1, i[1]))
                self.add(elem_list[pos])
                elem_list[pos] = 'checked'
            check_list = new_check_list


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = None
        elem = self._root
        while elem is not None:
            if elem.data > item:
                res = elem.data
                elem = elem.left
            else:
                elem = elem.right
        return res

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = None
        elem = self._root
        while elem is not None:
            if elem.data < item:
                res = elem.data
                elem = elem.right
            else:
                elem = elem.left
        return res

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding = 'utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]

        checked_lines = lines[:30000]
        random_words = []
        for i in range(10000):
            word = random.choice(checked_lines)
            random_words.append(word)
        with open('random_words.txt', 'w', encoding = 'utf-8') as file1:
            file1.write('\n'.join(random_words))

        self.clear()
        for line in checked_lines:
            self.add(line)

        # 1
        time1 = time.time()
        for i in random_words:
            checked_lines.index(i)
        print(f'Вбудовані методи типу list - {time.time()-time1} с.')

        # 2
        time1 = time.time()
        for i in random_words:
            self.find(i)
        print(f'Дерево в алфавітному порядку - {time.time()-time1} с.')

        # 3
        self.clear()
        random.shuffle(checked_lines)
        for line in checked_lines:
            self.add(line)
        time1 = time.time()
        for i in random_words:
            self.find(i)
        print(f'Дерево в довільному порядку - {time.time()-time1} с.')

        # 4
        self.rebalance()
        time1 = time.time()
        for i in random_words:
            self.find(i)
        print(f'Дерево після балансування - {time.time()-time1} с.')

if __name__=='__main__':
    el = LinkedBST()
    el.demo_bst('words.txt')
