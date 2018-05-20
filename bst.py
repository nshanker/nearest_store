class Node:
    def __init__(self, key, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.val = value

class BST:
    def __init__(self):
        self.root = None

    def get(self, key):
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.val
        return None

    def put(self, key, val=None):
        self.root = self._put(self.root, key, val)

    def _put(self, node, key, val):
        if node is None:
            node = Node(key, val)
            return node
        if key < node.key:
            node.left = self._put(node.left, key, val)
        elif key > node.key:
            node.right = self._put(node.right, key, val)
        else:
            node.val = val
        return node

    def closest(self, key):
        ''' Return both predecessor and successor ''' 
        x = self.get(key)
        if x:
            return x.val

        lo = self.floor(key)
        hi = self.ceil(key)

        if lo and hi: 
            return (lo.val, hi.val)
        elif lo is None:
            return (None, lo.val)
        elif hi is None:
            return (lo.val, None)
        else:
            return (None, None)



    def floor(self, key):
        return self._floor(self.root, key)

    def ceil(self, key):
        return self._ceil(self.root, key)

    def _floor(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node

        if key < node.key:
            return self._floor(node.left, key)
        else:
            t = self._floor(node.right, key)
            if t is None:
                return node
            else:
                return t

    def _ceil(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node

        if key > node.key:
            return self._ceil(node.right, key)
        else:
            t = self._ceil(node.left, key)
            if t is None:
                return node
            else:
                return t


