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

    def insert(self, key, value, expires_at=None):
        """
        Insere uma chave e valor na árvore. Se a chave já existir,
        atualiza o valor e o expires_at (comportamento upsert).
        Sempre inicia novos nós como RED e executa o rebalanceamento.
        """
        existing = self.search(key)
        if existing != self.NIL:
            existing.value = value
            existing.expires_at = expires_at
            return existing

        z = Node(key, value, expires_at, color="RED")
        z.left = self.NIL
        z.right = self.NIL

        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self._fix_insert(z)
        return z

    def _fix_insert(self, z):
        # Placeholder para o balanceamento (será implementado no Commit 5)
        # Por enquanto, apenas garante que se for a raiz da árvore, ela fica preta
        if z == self.root:
            z.color = "BLACK"


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

    def is_valid_rb_tree(self):
        """
        Valida se a árvore atual é uma Árvore Vermelho-Preto válida.
        Verifica as seguintes propriedades:
        1. A raiz é BLACK (se não for vazia).
        2. Nenhum nó RED possui filhos RED.
        3. Todos os caminhos de qualquer nó até as folhas NIL possuem o mesmo número de nós BLACK.
        4. Consistência dos ponteiros parent-child.
        """
        if self.root == self.NIL:
            return True

        if self.root.color != "BLACK":
            return False

        def check_properties(node):
            if node == self.NIL:
                return True, 1  # Retorna (é_valido, altura_preta)

            # Propriedade: nó vermelho não pode ter filhos vermelhos
            if node.color == "RED":
                if (node.left != self.NIL and node.left.color == "RED") or \
                   (node.right != self.NIL and node.right.color == "RED"):
                    return False, 0

            # Validação dos ponteiros de parentesco
            if node.left != self.NIL and node.left.parent != node:
                return False, 0
            if node.right != self.NIL and node.right.parent != node:
                return False, 0

            left_valid, left_black_height = check_properties(node.left)
            if not left_valid:
                return False, 0

            right_valid, right_black_height = check_properties(node.right)
            if not right_valid:
                return False, 0

            # Propriedade: caminhos para as folhas devem ter a mesma altura preta
            if left_black_height != right_black_height:
                return False, 0

            # Calcula altura preta do nó atual
            current_black_height = left_black_height + (1 if node.color == "BLACK" else 0)
            return True, current_black_height

        valid, _ = check_properties(self.root)
        return valid


