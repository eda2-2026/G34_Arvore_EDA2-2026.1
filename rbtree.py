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

    def left_rotate(self, x):
        """
        Rotaciona à esquerda sobre o nó x.
        """
        y = x.right
        if y == self.NIL:
            return  # Não é possível rotacionar se o filho direito for NIL
        
        # O filho esquerdo de y vira filho direito de x
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
            
        # O pai de x passa a ser pai de y
        y.parent = x.parent
        if x.parent == self.NIL or x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        # x vira filho esquerdo de y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        """
        Rotaciona à direita sobre o nó x.
        """
        y = x.left
        if y == self.NIL:
            return  # Não é possível rotacionar se o filho esquerdo for NIL
            
        # O filho direito de y vira filho esquerdo de x
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
            
        # O pai de x passa a ser pai de y
        y.parent = x.parent
        if x.parent == self.NIL or x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
            
        # x vira filho direito de y
        y.right = x
        x.parent = y

