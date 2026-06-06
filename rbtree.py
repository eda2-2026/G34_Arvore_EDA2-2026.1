# rbtree.py

class Node:
    def __init__(self, key=None, value=None, expires_at=None, color="RED"):
        self.key = key
        self.value = value
        self.expires_at = expires_at  # Timestamp Unix em milissegundos
        self.color = color            # "RED" ou "BLACK"
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return f"Node({self.key}, {self.color})"


class RedBlackTree:
    def __init__(self):
        # NIL representa as folhas nulas (sentinelas) da árvore, que são sempre pretas
        self.NIL = Node(color="BLACK")
        self.root = self.NIL

    def search(self, key):
        """
        Busca uma chave na árvore lexicograficamente.
        Retorna o nó se encontrado, ou self.NIL caso contrário.
        """
        curr = self.root
        while curr != self.NIL:
            if key == curr.key:
                return curr
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return self.NIL
