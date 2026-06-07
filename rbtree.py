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
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL

    def minimum(self, node):
        """
        Retorna o nó com a menor chave a partir do nó fornecido.
        """
        curr = node
        while curr.left != self.NIL:
            curr = curr.left
        return curr

    def _transplant(self, u, v):
        """
        Substitui a subárvore enraizada no nó u pela subárvore enraizada no nó v.
        """
        if u.parent == self.NIL or u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        
        v.parent = u.parent

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
        """
        Corrige as violações das propriedades da Árvore Vermelho-Preto após inserção.
        Garante que não existam dois nós vermelhos consecutivos e que a raiz permaneça preta.
        """
        while z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # Tio de z
                if y.color == "RED":
                    # Caso 1: Tio é vermelho -> Recolorir pai, tio e avô
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    # Caso 2: Tio é preto e z é filho direito
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    # Caso 3: Tio é preto e z é filho esquerdo
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left  # Tio de z
                if y.color == "RED":
                    # Caso 1 (simétrico): Tio é vermelho
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    # Caso 2 (simétrico): Tio é preto e z é filho esquerdo
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    # Caso 3 (simétrico): Tio é preto e z é filho direito
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.left_rotate(z.parent.parent)
        self.root.color = "BLACK"

    def delete(self, key):
        """
        Deleta um nó com a chave correspondente da árvore.
        Retorna o nó deletado se encontrado, ou None caso contrário.
        """
        z = self.search(key)
        if z == self.NIL:
            return None

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self._fix_delete(x)

        return z

    def _fix_delete(self, x):
        """
        Corrige as violações das propriedades da Árvore Vermelho-Preto após deleção.
        Trata os 4 casos clássicos de violação de cor/altura preta e suas versões simétricas.
        """
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right  # irmão de x
                if w.color == "RED":
                    # Caso 1: irmão é vermelho
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    # Caso 2: filhos do irmão são pretos
                    w.color = "RED"
                    x = x.parent
                else:
                    # Caso 3: filho esquerdo do irmão é vermelho, direito é preto
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self.right_rotate(w)
                        w = x.parent.right
                    # Caso 4: filho direito do irmão é vermelho
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left  # irmão de x (simétrico)
                if w.color == "RED":
                    # Caso 1 (simétrico): irmão é vermelho
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    # Caso 2 (simétrico): filhos do irmão são pretos
                    w.color = "RED"
                    x = x.parent
                else:
                    # Caso 3 (simétrico): filho direito do irmão é vermelho, esquerdo é preto
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self.left_rotate(w)
                        w = x.parent.left
                    # Caso 4 (simétrico): filho esquerdo do irmão é vermelho
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"


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


