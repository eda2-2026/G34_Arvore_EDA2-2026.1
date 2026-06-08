# cache.py
import time
from rbtree import RedBlackTree


class TTLCache:
    """
    In-memory TTL cache backed by a Red-Black Tree.

    Supports set/get/delete with lazy expiration, bulk purge of expired
    entries via in-order traversal, and usage statistics.
    """

    def __init__(self):
        self._tree = RedBlackTree()
        self._ttl_misses = 0
        self._total_ops = 0

    def _now_ms(self):
        """Return the current Unix timestamp in milliseconds."""
        return time.time_ns() // 1_000_000

    def set(self, key, value, ttl_ms):
        """
        Insert or update a key with a TTL in milliseconds.

        If ttl_ms is None, the entry never expires (expires_at = None).
        If the key already exists, the value and expiration are updated.
        Returns the underlying Node.
        """
        if ttl_ms is None:
            expires_at = None
        else:
            expires_at = self._now_ms() + ttl_ms
        node = self._tree.insert(key, value, expires_at)
        self._total_ops += 1
        return node

    def get(self, key):
        """
        Retrieve a value by key.

        Returns the value if the key exists and has not expired.
        If the key is expired, it is lazily deleted and None is returned.
        If the key does not exist, None is returned.
        Entries with expires_at=None never expire.
        """
        self._total_ops += 1
        node = self._tree.search(key)
        if node == self._tree.NIL:
            return None
        if node.expires_at is not None and self._now_ms() >= node.expires_at:
            self._tree.delete(key)
            self._ttl_misses += 1
            return None
        return node.value

    def delete(self, key):
        """
        Delete a key from the cache.

        Returns True if the key was found and deleted, False otherwise.
        """
        self._total_ops += 1
        deleted = self._tree.delete(key)
        return deleted is not None

    def purge(self):
        """
        Remove all expired entries via in-order traversal.

        Returns the number of entries removed.
        """
        self._total_ops += 1
        now = self._now_ms()
        expired_keys = []
        for node in self._tree.inorder():
            if node.expires_at is not None and now >= node.expires_at:
                expired_keys.append(node.key)
        for key in expired_keys:
            self._tree.delete(key)
        return len(expired_keys)

    def get_stats(self):
        """
        Return usage statistics as a dict.

        Computes live_entries by counting non-expired nodes via in-order
        traversal (triggers lazy cleanup for expired entries found during
        the traversal). Increments total_ops.
        """
        self._total_ops += 1
        now = self._now_ms()
        live_entries = 0
        for node in self._tree.inorder():
            if node.expires_at is None or now < node.expires_at:
                live_entries += 1
        return {
            "live_entries": live_entries,
            "ttl_misses": self._ttl_misses,
            "total_ops": self._total_ops,
        }
