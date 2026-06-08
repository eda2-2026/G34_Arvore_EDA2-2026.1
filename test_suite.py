# test_suite.py
import io
import unittest
from unittest.mock import patch
from rbtree import RedBlackTree, Node
from cache import TTLCache
import cli

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


class TestRedBlackTreeInsertRebalance(unittest.TestCase):
    def test_insert_ordered_asc(self):
        tree = RedBlackTree()
        keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        for i, key in enumerate(keys):
            tree.insert(key, f"val_{i}")
            self.assertTrue(tree.is_valid_rb_tree(), f"Failed after inserting {key}")

    def test_insert_ordered_desc(self):
        tree = RedBlackTree()
        keys = ["j", "i", "h", "g", "f", "e", "d", "c", "b", "a"]
        for i, key in enumerate(keys):
            tree.insert(key, f"val_{i}")
            self.assertTrue(tree.is_valid_rb_tree(), f"Failed after inserting {key}")

    def test_insert_random(self):
        import random
        random.seed(42)
        tree = RedBlackTree()
        keys = list(range(100))
        random.shuffle(keys)
        for key in keys:
            tree.insert(key, f"val_{key}")
            self.assertTrue(tree.is_valid_rb_tree(), f"Failed after inserting {key}")


class TestRedBlackTreeLimits(unittest.TestCase):
    def test_insert_large_volume(self):
        tree = RedBlackTree()
        # Inserir 1000 chaves e garantir validade estrutural contínua
        for i in range(1000):
            tree.insert(f"key_{i}", i)
        self.assertTrue(tree.is_valid_rb_tree())
        
        # Testar busca rápida em grande volume
        node = tree.search("key_500")
        self.assertNotEqual(node, tree.NIL)
        self.assertEqual(node.value, 500)


class TestRedBlackTreeMinimum(unittest.TestCase):
    def test_minimum_on_subtree(self):
        tree = RedBlackTree()
        # Inserir alguns elementos manualmente para testar o mínimo
        r = tree.insert("m", "val_m")
        l = tree.insert("e", "val_e")
        rg = tree.insert("t", "val_t")
        l_l = tree.insert("b", "val_b")
        l_r = tree.insert("g", "val_g")
        
        # O mínimo da árvore inteira deve ser "b"
        self.assertEqual(tree.minimum(tree.root), l_l)
        # O mínimo da subárvore direita a partir de "m" deve ser "t"
        self.assertEqual(tree.minimum(rg), rg)
        # O mínimo da subárvore esquerda a partir de "e" deve ser "b"
        self.assertEqual(tree.minimum(l), l_l)


class TestRedBlackTreeBasicDelete(unittest.TestCase):
    def test_delete_non_existent(self):
        tree = RedBlackTree()
        self.assertIsNone(tree.delete("non_existent"))

    def test_delete_single_root(self):
        tree = RedBlackTree()
        node = tree.insert("root_key", "val")
        deleted = tree.delete("root_key")
        self.assertEqual(deleted, node)
        self.assertEqual(tree.root, tree.NIL)
        self.assertTrue(tree.is_valid_rb_tree())

    def test_delete_red_leaf(self):
        tree = RedBlackTree()
        r = tree.insert("m", "val_m")
        l = tree.insert("a", "val_a") # Deve ser vermelho
        
        self.assertEqual(l.color, "RED")
        deleted = tree.delete("a")
        self.assertEqual(deleted, l)
        self.assertEqual(tree.root, r)
        self.assertEqual(r.left, tree.NIL)
        self.assertTrue(tree.is_valid_rb_tree())


class TestRedBlackTreeDeleteRebalance(unittest.TestCase):
    def test_delete_black_leaf_trigger_rebalance(self):
        tree = RedBlackTree()
        tree.insert("d", 4)
        tree.insert("b", 2)
        tree.insert("f", 6)
        tree.insert("a", 1)
        tree.insert("c", 3)
        tree.insert("e", 5)
        tree.insert("g", 7)
        
        self.assertTrue(tree.is_valid_rb_tree())
        
        for key in ["a", "b", "c", "d", "e", "f", "g"]:
            tree.delete(key)
            self.assertTrue(tree.is_valid_rb_tree(), f"Failed after deleting {key}")

    def test_delete_random_large(self):
        import random
        random.seed(100)
        tree = RedBlackTree()
        keys = list(range(200))
        random.shuffle(keys)
        
        for key in keys:
            tree.insert(key, f"val_{key}")
            
        self.assertTrue(tree.is_valid_rb_tree())
        
        random.shuffle(keys)
        for key in keys:
            deleted = tree.delete(key)
            self.assertIsNotNone(deleted)
            self.assertEqual(deleted.key, key)
            self.assertTrue(tree.is_valid_rb_tree(), f"Failed after deleting {key}")
            
        self.assertEqual(tree.root, tree.NIL)


class TestTTLCacheBasic(unittest.TestCase):
    """Task 6: Basic set/get/delete operations on TTLCache."""

    def setUp(self):
        self.cache = TTLCache()

    def test_set_and_get(self):
        self.cache.set("name", "Alice", 5000)
        self.assertEqual(self.cache.get("name"), "Alice")

    def test_get_non_existent(self):
        self.assertIsNone(self.cache.get("ghost"))

    def test_upsert_existing_key(self):
        node1 = self.cache.set("key", "old", 5000)
        node2 = self.cache.set("key", "new", 9999)
        # Same underlying node
        self.assertIs(node1, node2)
        self.assertEqual(node1.value, "new")
        self.assertEqual(node1.expires_at, node2.expires_at)
        self.assertEqual(self.cache.get("key"), "new")

    def test_delete_existing(self):
        self.cache.set("x", 10, 5000)
        self.assertTrue(self.cache.delete("x"))
        self.assertIsNone(self.cache.get("x"))

    def test_delete_non_existent(self):
        self.assertFalse(self.cache.delete("nope"))


class TestTTLCacheExpiration(unittest.TestCase):
    """Task 7: TTL expiration and lazy deletion."""

    def setUp(self):
        self.cache = TTLCache()
        self._fake_now = 1000000

    def _patch_now(self):
        """Monkey-patch _now_ms to return controllable fake time."""
        cache = self.cache

        def fake_now_ms():
            return self._fake_now

        return patch.object(cache, "_now_ms", fake_now_ms)

    def test_lazy_expiration(self):
        with self._patch_now():
            self.cache.set("ephemeral", "data", ttl_ms=100)
            # Before expiry
            self.assertEqual(self.cache.get("ephemeral"), "data")
            # Advance time past ttl
            self._fake_now += 200
            # Now it should be expired and deleted lazily
            self.assertIsNone(self.cache.get("ephemeral"))
            # Node should be gone from tree
            self.assertIsNone(self.cache.get("ephemeral"))

    def test_expired_ttl_miss_count(self):
        with self._patch_now():
            self.cache.set("a", 1, ttl_ms=50)
            self.cache.set("b", 2, ttl_ms=500)
            self._fake_now += 200  # a expired, b still valid
            self.assertIsNone(self.cache.get("a"))   # ttl_miss
            self.assertEqual(self.cache.get("b"), 2)  # valid
            self.assertEqual(self.cache._ttl_misses, 1)

    def test_no_expiration(self):
        """Entries with ttl_ms=None never expire."""
        with self._patch_now():
            self.cache.set("permanent", "forever", ttl_ms=None)
            self._fake_now += 999999
            self.assertEqual(self.cache.get("permanent"), "forever")


class TestTTLCachePurge(unittest.TestCase):
    """Task 8: Bulk purge of expired entries via in-order traversal."""

    def setUp(self):
        self.cache = TTLCache()
        self._fake_now = 1000000

    def _patch_now(self):
        cache = self.cache

        def fake_now_ms():
            return self._fake_now

        return patch.object(cache, "_now_ms", fake_now_ms)

    def test_purge_removes_expired(self):
        with self._patch_now():
            self.cache.set("a", 1, ttl_ms=100)
            self.cache.set("b", 2, ttl_ms=1000)
            self.cache.set("c", 3, ttl_ms=100)
            # Advance time so a and c expire, b stays
            self._fake_now += 500
            removed = self.cache.purge()
            self.assertEqual(removed, 2)
            # a and c should be gone
            self.assertIsNone(self.cache.get("a"))
            self.assertIsNone(self.cache.get("c"))
            # b should still be present
            self.assertEqual(self.cache.get("b"), 2)

    def test_purge_returns_count(self):
        with self._patch_now():
            self.cache.set("x", 1, ttl_ms=10)
            self.cache.set("y", 2, ttl_ms=10)
            self._fake_now += 50
            removed = self.cache.purge()
            self.assertEqual(removed, 2)

    def test_purge_empty_cache(self):
        with self._patch_now():
            removed = self.cache.purge()
            self.assertEqual(removed, 0)


class TestTTLCacheStats(unittest.TestCase):
    """Task 9: Statistics tracking."""

    def setUp(self):
        self.cache = TTLCache()
        self._fake_now = 1000000

    def _patch_now(self):
        cache = self.cache

        def fake_now_ms():
            return self._fake_now

        return patch.object(cache, "_now_ms", fake_now_ms)

    def test_stats_counts(self):
        with self._patch_now():
            # Perform operations
            self.cache.set("k1", "v1", ttl_ms=200)
            self.cache.set("k2", "v2", ttl_ms=200)
            self.cache.get("k1")   # valid get
            self.cache.get("k3")   # non-existent
            self._fake_now += 300  # both expire
            self.cache.get("k1")   # ttl miss (lazy)
            self.cache.delete("k2")  # delete existing

            stats = self.cache.get_stats()
            # Ops: 2 sets + 3 gets + 1 delete + 1 get_stats = 7
            self.assertEqual(stats["total_ops"], 7)
            self.assertEqual(stats["ttl_misses"], 1)
            # k1 expired and lazily deleted, k2 manually deleted → 0 live
            self.assertEqual(stats["live_entries"], 0)


class TestCLI(unittest.TestCase):
    """Task 10: Interactive CLI command processing."""

    def setUp(self):
        self.cache = TTLCache()
        self._fake_now = 1000000

    def _run_cli(self, commands):
        """Simulate CLI input and capture output."""
        input_str = "\n".join(commands)
        with patch("sys.stdin", io.StringIO(input_str)):
            with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                with patch("cli.TTLCache", return_value=self.cache):
                    cli.main()
                return fake_out.getvalue()

    def test_set_and_get(self):
        output = self._run_cli([
            "SET name Alice 5000",
            "GET name",
            "EXIT",
        ])
        lines = output.strip().split("\n")
        self.assertEqual(lines[0], "OK")
        self.assertEqual(lines[1], "Alice")

    def test_delete(self):
        output = self._run_cli([
            "SET temp data 10000",
            "DELETE temp",
            "DELETE temp",
            "EXIT",
        ])
        lines = output.strip().split("\n")
        self.assertEqual(lines[0], "OK")
        self.assertEqual(lines[1], "OK")
        self.assertEqual(lines[2], "MISS")

    def test_purge_and_stats(self):
        output = self._run_cli([
            "SET a 1 100",
            "PURGE",
            "STATS",
            "EXIT",
        ])
        lines = output.strip().split("\n")
        # SET → OK
        self.assertEqual(lines[0], "OK")
        # PURGE returns 0 (not expired yet in real time)
        self.assertIn("Removed 0 expired entries", lines[1])
        # STATS should show live_entries, ttl_misses, total_ops
        self.assertIn("Live entries:", lines[2])
        self.assertIn("TTL misses:", lines[3])
        self.assertIn("Total ops:", lines[4])

    def test_unknown_command(self):
        output = self._run_cli([
            "FOOBAR",
            "EXIT",
        ])
        self.assertIn("Unknown command: FOOBAR", output)

    def test_missing_args(self):
        output = self._run_cli([
            "SET onlytwo",
            "GET",
            "DELETE",
            "EXIT",
        ])
        self.assertIn("Usage: SET <key> <value> <ttl_ms>", output)
        self.assertIn("Usage: GET <key>", output)
        self.assertIn("Usage: DELETE <key>", output)


if __name__ == "__main__":
    unittest.main()







