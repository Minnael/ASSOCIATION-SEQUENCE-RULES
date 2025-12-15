# apriori.py
from itertools import combinations


def calcular_suporte(conjunto_itens, transacoes):
    """
    Calcula o suporte de um conjunto de itens.
    Suporte = (número de transações que contêm o conjunto) / total de transações.
    """
    transacoes_totais = len(transacoes)
    ocorrencias = sum(1 for transacao in transacoes if conjunto_itens.issubset(transacao))
    return ocorrencias / transacoes_totais


def gerar_candidatos(itemsets_frequentes_anterior, tamanho_itemset):
    """
    Gera candidatos Ck combinando itemsets frequentes de tamanho k-1.
    Exemplo: L2 → gera C3.
    
    Regras da combinação:
    - junta dois itemsets com (k-2) itens iguais
    - o itemset resultante deve ter tamanho exato = k
    """
    candidatos = set()
    lista_itemsets = list(itemsets_frequentes_anterior)

    for i in range(len(lista_itemsets)):
        for j in range(i + 1, len(lista_itemsets)):
            uniao = lista_itemsets[i].union(lista_itemsets[j])

            # Só aceita a união se ela gerar um itemset do tamanho desejado
            if len(uniao) == tamanho_itemset:
                candidatos.add(frozenset(uniao))

    return candidatos


def apriori(transacoes, suporte_minimo):
    """
    Implementação completa do algoritmo Apriori.
    Retorna uma lista de níveis L1, L2, L3, ... contendo os itemsets frequentes.
    """

    # --- 1) Encontrar L1 (itemsets de tamanho 1 frequentes)
    itens_unicos = set().union(*transacoes)  # todos os itens presentes no dataset

    L1 = [
        frozenset([item])
        for item in itens_unicos
        if calcular_suporte({item}, transacoes) >= suporte_minimo
    ]

    lista_niveis = [L1]  # L1 armazenado como o primeiro nível de itemsets frequentes
    k = 2  # agora começaremos a gerar itemsets de tamanho 2

    while True:
        # --- 2) Gerar candidatos Ck a partir de L(k-1)
        candidatos_k = gerar_candidatos(lista_niveis[k - 2], k)

        # --- 3) Filtrar apenas aqueles que atingem o suporte mínimo → Lk
        frequentes_k = [
            conjunto
            for conjunto in candidatos_k
            if calcular_suporte(conjunto, transacoes) >= suporte_minimo
        ]

        # Se nenhum itemset de tamanho k é frequente → parar o algoritmo
        if not frequentes_k:
            break

        # Adicionar o nível encontrado na lista principal e continuar
        lista_niveis.append(frequentes_k)
        k += 1

    return lista_niveis


def gerar_regras(itemsets_por_nivel, transacoes, confianca_minima):
    """
    Gera regras de associação a partir dos itemsets frequentes.
    
    Para cada itemset frequente Lk (k >= 2), gera regras do tipo:
        A → B
    onde:
        A está contido em itemset
        B = itemset - A
        confiança = suporte(itemset) / suporte(A)
    """
    regras = []

    # pula L1, porque regras só são possíveis a partir de L2
    for nivel in itemsets_por_nivel[1:]:
        for itemset in nivel:
            tamanho = len(itemset)

            # gerar todas as divisões possíveis A → B
            for tamanho_A in range(1, tamanho):
                for subconjunto_A in combinations(itemset, tamanho_A):

                    A = frozenset(subconjunto_A)
                    B = itemset - A

                    suporte_itemset = calcular_suporte(itemset, transacoes)
                    suporte_A = calcular_suporte(A, transacoes)
                    confianca = suporte_itemset / suporte_A

                    if confianca >= confianca_minima:
                        regras.append((A, B, confianca, suporte_itemset))

    return regras
