# test_suite.py
import unittest
from rbtree import RedBlackTree, Node

class TestRedBlackTreeRotations(unittest.TestCase):
    def test_left_rotate(self):
        tree = RedBlackTree()
        # Montar manualmente uma árvore para testar rotação:
        #      x
        #     / \
        #    a   y
        #       / \
        #      b   c
        x = Node("x")
        a = Node("a")
        y = Node("y")
        b = Node("b")
        c = Node("c")
        
        tree.root = x
        x.parent = tree.NIL
        
        x.left = a; a.parent = x
        x.right = y; y.parent = x
        
        y.left = b; b.parent = y
        y.right = c; c.parent = y
        
        a.left = tree.NIL; a.right = tree.NIL
        b.left = tree.NIL; b.right = tree.NIL
        c.left = tree.NIL; c.right = tree.NIL
        
        # Executar rotação à esquerda em x
        tree.left_rotate(x)
        
        # A árvore resultante deve ser:
        #      y
        #     / \
        #    x   c
        #   / \
        #  a   b
        self.assertEqual(tree.root, y)
        self.assertEqual(y.parent, tree.NIL)
        
        self.assertEqual(y.left, x)
        self.assertEqual(x.parent, y)
        
        self.assertEqual(y.right, c)
        self.assertEqual(c.parent, y)
        
        self.assertEqual(x.left, a)
        self.assertEqual(a.parent, x)
        
        self.assertEqual(x.right, b)
        self.assertEqual(b.parent, x)

    def test_right_rotate(self):
        tree = RedBlackTree()
        # Montar manualmente uma árvore para testar rotação:
        #      y
        #     / \
        #    x   c
        #   / \
        #  a   b
        y = Node("y")
        x = Node("x")
        c = Node("c")
        a = Node("a")
        b = Node("b")
        
        tree.root = y
        y.parent = tree.NIL
        
        y.left = x; x.parent = y
        y.right = c; c.parent = y
        
        x.left = a; a.parent = x
        x.right = b; b.parent = x
        
        a.left = tree.NIL; a.right = tree.NIL
        b.left = tree.NIL; b.right = tree.NIL
        c.left = tree.NIL; c.right = tree.NIL
        
        # Executar rotação à direita em y
        tree.right_rotate(y)
        
        # A árvore resultante deve ser:
        #      x
        #     / \
        #    a   y
        #       / \
        #      b   c
        self.assertEqual(tree.root, x)
        self.assertEqual(x.parent, tree.NIL)
        
        self.assertEqual(x.left, a)
        self.assertEqual(a.parent, x)
        
        self.assertEqual(x.right, y)
        self.assertEqual(y.parent, x)
        
        self.assertEqual(y.left, b)
        self.assertEqual(b.parent, y)
        
        self.assertEqual(y.right, c)
        self.assertEqual(c.parent, y)

    def test_search_empty(self):
        tree = RedBlackTree()
        self.assertEqual(tree.search("key"), tree.NIL)


class TestRedBlackTreeValidation(unittest.TestCase):
    def test_empty_tree_is_valid(self):
        tree = RedBlackTree()
        self.assertTrue(tree.is_valid_rb_tree())

    def test_single_black_root_is_valid(self):
        tree = RedBlackTree()
        root = Node("root", color="BLACK")
        root.left = tree.NIL
        root.right = tree.NIL
        root.parent = tree.NIL
        tree.root = root
        self.assertTrue(tree.is_valid_rb_tree())

    def test_red_root_is_invalid(self):
        tree = RedBlackTree()
        root = Node("root", color="RED")
        root.left = tree.NIL
        root.right = tree.NIL
        root.parent = tree.NIL
        tree.root = root
        self.assertFalse(tree.is_valid_rb_tree())

    def test_consecutive_red_nodes_is_invalid(self):
        tree = RedBlackTree()
        root = Node("root", color="BLACK")
        left = Node("left", color="RED")
        left_left = Node("left_left", color="RED")

        tree.root = root
        root.parent = tree.NIL
        root.right = tree.NIL

        root.left = left
        left.parent = root
        left.right = tree.NIL

        left.left = left_left
        left_left.parent = left
        left_left.left = tree.NIL
        left_left.right = tree.NIL

        self.assertFalse(tree.is_valid_rb_tree())

    def test_different_black_heights_is_invalid(self):
        tree = RedBlackTree()
        root = Node("root", color="BLACK")
        left = Node("left", color="BLACK")

        tree.root = root
        root.parent = tree.NIL
        root.right = tree.NIL

        root.left = left
        left.parent = root
        left.left = tree.NIL
        left.right = tree.NIL

        self.assertFalse(tree.is_valid_rb_tree())

    def test_invalid_parent_pointer_is_invalid(self):
        tree = RedBlackTree()
        root = Node("root", color="BLACK")
        left = Node("left", color="RED")

        tree.root = root
        root.parent = tree.NIL
        root.right = tree.NIL
        root.left = left
        left.parent = tree.NIL  # Deveria ser root
        left.left = tree.NIL
        left.right = tree.NIL

        self.assertFalse(tree.is_valid_rb_tree())


class TestRedBlackTreeBasicInsert(unittest.TestCase):
    def test_insert_single_node(self):
        tree = RedBlackTree()
        node = tree.insert("key1", "val1", 1000)
        self.assertEqual(tree.root, node)
        self.assertEqual(node.key, "key1")
        self.assertEqual(node.value, "val1")
        self.assertEqual(node.expires_at, 1000)
        self.assertEqual(node.color, "BLACK")
        self.assertEqual(node.left, tree.NIL)
        self.assertEqual(node.right, tree.NIL)
        self.assertEqual(node.parent, tree.NIL)

    def test_insert_multiple_bst_structure(self):
        tree = RedBlackTree()
        # Sem balanceamento real por enquanto (apenas BST clássica)
        r = tree.insert("m", "root_val")
        l = tree.insert("a", "left_val")
        rg = tree.insert("z", "right_val")
        
        self.assertEqual(tree.root, r)
        self.assertEqual(r.left, l)
        self.assertEqual(r.right, rg)
        self.assertEqual(l.parent, r)
        self.assertEqual(rg.parent, r)
        self.assertEqual(l.left, tree.NIL)
        self.assertEqual(rg.right, tree.NIL)

    def test_upsert_existing_key(self):
        tree = RedBlackTree()
        node1 = tree.insert("key1", "val1", 1000)
        node2 = tree.insert("key1", "val2", 2000)
        
        # O nó retornado deve ser o mesmo
        self.assertEqual(node1, node2)
        # O valor e o TTL devem ter sido atualizados
        self.assertEqual(node1.value, "val2")
        self.assertEqual(node1.expires_at, 2000)
        # A árvore deve conter apenas um nó
        self.assertEqual(tree.root, node1)
        self.assertEqual(tree.root.left, tree.NIL)
        self.assertEqual(tree.root.right, tree.NIL)


if __name__ == "__main__":
    unittest.main()


