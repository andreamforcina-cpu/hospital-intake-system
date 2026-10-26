"""Binary reporting tree; placement follows management, not alphabetical order."""


class DoctorNode:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class DoctorTree:
    def __init__(self):
        self.root = None

    def _find(self, node, name):
        if node is None or node.name == name:
            return node
        return self._find(node.left, name) or self._find(node.right, name)

    def insert(self, parent_name, employee_name, side):
        """Return False for missing parents, invalid sides, or occupied slots."""
        if side not in ('left', 'right'):
            return False
        parent = self._find(self.root, parent_name)
        if parent is None or getattr(parent, side) is not None:
            return False
        # Names identify doctors, so duplicates would make parent lookup ambiguous.
        if self._find(self.root, employee_name) is not None:
            return False
        setattr(parent, side, DoctorNode(employee_name))
        return True

    def preorder(self, node):
        if node is None:
            return []
        return [node.name] + self.preorder(node.left) + self.preorder(node.right)

    def inorder(self, node):
        if node is None:
            return []
        return self.inorder(node.left) + [node.name] + self.inorder(node.right)

    def postorder(self, node):
        if node is None:
            return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.name]


if __name__ == '__main__':
    tree = DoctorTree()
    tree.root = DoctorNode('Dr. Croft')
    tree.insert('Dr. Croft', 'Dr. Goldsmith', 'right')
    tree.insert('Dr. Croft', 'Dr. Phan', 'left')
    tree.insert('Dr. Phan', 'Dr. Carson', 'right')
    tree.insert('Dr. Phan', 'Dr. Morgan', 'left')
    print(tree.preorder(tree.root))
    print(tree.inorder(tree.root))
    print(tree.postorder(tree.root))
