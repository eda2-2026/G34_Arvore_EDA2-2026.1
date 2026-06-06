# Sistema de Cache com TTL usando Arvore Vermelho-Preto (Red-Black Tree)

Este projeto consiste na implementacao de um cache em memoria com suporte a expiracao de tempo de vida (TTL - Time-To-Live), utilizando uma Arvore Vermelho-Preto (Red-Black Tree) desenvolvida do zero em Python como a estrutura de indexacao principal. 

O sistema replica comportamentos basicos encontrados em bancos de dados em memoria, como o Redis e o Memcached.

---

## Por que usar uma Arvore Vermelho-Preto?

A Red-Black Tree eh uma arvore de busca binaria auto-balanceada que garante complexidade de tempo de pior caso de O(log n) para operacoes de busca, insercao e remocao.

Diferente de tabelas Hash convencionais, as chaves na RB Tree ficam ordenadas lexicograficamente (alfabeticamente). Essa ordenacao nos permite:
1. Evitar a degradacao: Tabelas hash podem degenerar para O(n) se houver colisoes excessivas.
2. Varredura eficiente (Range Queries): Percorrer intervalos de chaves ou realizar limpezas sequenciais de maneira eficiente em O(k log n), ideal para a operacao de PURGE em lote.

---

## Estrutura de Arquivos

O projeto esta modularizado da seguinte forma:

*   **rbtree.py**: Contem a logica estrutural da Arvore Vermelho-Preto (Node e RedBlackTree), como as rotacoes, busca e, posteriormente, insercao, remocao fisica e rebalanceamento estrutural.
*   **cache.py**: Define a interface TTLCache, que gerencia o calculo do tempo Unix em milissegundos, as regras de negocio de expiracao (remocao preguicosa e purge) e estatisticas.
*   **cli.py**: Fornece uma interface de linha de comando interativa para comunicacao direta no terminal.
*   **test_suite.py**: Suite de testes automatizados unitarios usando o framework nativo unittest do Python.

---

## Requisitos e Execucao

### Pre-requisitos
*   Python 3.8 ou superior instalado.
*   Nenhuma biblioteca adicional externa eh necessaria (utiliza-se apenas bibliotecas embutidas do Python).

### Como rodar os Testes Unitarios
Para rodar os testes unitarios e garantir que toda a logica da arvore esteja funcionando perfeitamente:
```bash
python test_suite.py
```

### Como rodar a CLI Interativa (Apos implementacao da Fase 5)
```bash
python cli.py
```

Comandos aceitos na CLI:
*   `SET <key> <value> <ttl_ms>`: Adiciona ou atualiza uma chave com valor e tempo de expiracao em milissegundos.
*   `GET <key>`: Retorna o valor associado se a chave for valida. Se estiver expirada, remove-a e retorna MISS.
*   `DELETE <key>`: Remove manualmente a chave indicada do cache.
*   `PURGE`: Varre a arvore de forma in-order e remove todas as chaves cujos prazos de validade ja expiraram.
*   `STATS`: Exibe estatisticas de uso (entradas vivas, misses por TTL, operacoes totais).

---

## Propriedades da Arvore Vermelho-Preto Mantidas
1. Todo no eh vermelho (RED) ou preto (BLACK).
2. A raiz da arvore eh sempre preta.
3. Nenhum no vermelho possui filhos vermelhos (restricao vermelho-vermelho).
4. Todo caminho simples de um no a qualquer uma de suas folhas descendentes NIL contem o mesmo numero de nos pretos (altura preta consistente).
