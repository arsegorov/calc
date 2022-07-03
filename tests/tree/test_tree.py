from calc.tree import Tree


def test_init():
    root = Tree()
    assert root.left == None
    assert root.right == None

def test_getters():
    left = Tree()
    right = Tree()
    root = Tree(left, right)
    assert root.left == left
    assert root.right == right

def test_setters():
    left = Tree()
    right = Tree()
    root = Tree()
    root.left = left
    root.right = right
    assert root.left == left
    assert root.right == right
