from collections import Counter
from itertools import combinations

# -----------------------------
# Base de transações
# -----------------------------
transacoes = [
    {'a', 'b'},
    {'b', 'c', 'd'},
    {'a', 'c', 'd', 'e'},
    {'a', 'd', 'e'},
    {'a', 'b', 'c'},
    {'a', 'b', 'c', 'd'},
    {'a'},
    {'a', 'b', 'c'},
    {'a', 'b', 'd'},
    {'b', 'c', 'e'}
]

phi = 2  # suporte mínimo
confianca_minima = 0.6
num_transacoes = len(transacoes)

# -----------------------------
# Estrutura do nó da FP-Tree
# -----------------------------
class NoFP:
    def __init__(self, item, pai):
        self.item = item
        self.contador = 1
        self.pai = pai
        self.filhos = {}
        self.link = None

# -----------------------------
# Construção da FP-Tree
# -----------------------------
def construir_fp_tree(transacoes, phi):
    contagem = Counter()
    for t in transacoes:
        contagem.update(t)

    itens_frequentes = {i: c for i, c in contagem.items() if c >= phi}
    ordem = sorted(itens_frequentes, key=lambda x: itens_frequentes[x], reverse=True)

    raiz = NoFP(None, None)
    tabela_header = {i: None for i in ordem}

    def inserir(itens, no_atual):
        if not itens:
            return
        primeiro = itens[0]
        if primeiro in no_atual.filhos:
            no_atual.filhos[primeiro].contador += 1
        else:
            novo_no = NoFP(primeiro, no_atual)
            no_atual.filhos[primeiro] = novo_no

            if tabela_header[primeiro] is None:
                tabela_header[primeiro] = novo_no
            else:
                aux = tabela_header[primeiro]
                while aux.link:
                    aux = aux.link
                aux.link = novo_no

        inserir(itens[1:], no_atual.filhos[primeiro])

    for t in transacoes:
        ordenada = [i for i in ordem if i in t]
        inserir(ordenada, raiz)

    return tabela_header

# -----------------------------
# Mineração FP-Growth
# -----------------------------
def minerar_fp_growth(tabela_header, phi, sufixo, padroes):
    for item in tabela_header:
        padrao_atual = sufixo + [item]

        suporte = 0
        no = tabela_header[item]
        while no:
            suporte += no.contador
            no = no.link

        if suporte >= phi:
            padroes[frozenset(padrao_atual)] = suporte

        caminhos_condicionais = []
        no = tabela_header[item]
        while no:
            caminho = []
            pai = no.pai
            while pai and pai.item:
                caminho.append(pai.item)
                pai = pai.pai
            for _ in range(no.contador):
                caminhos_condicionais.append(set(caminho))
            no = no.link

        if caminhos_condicionais:
            nova_tabela = construir_fp_tree(caminhos_condicionais, phi)
            if nova_tabela:
                minerar_fp_growth(nova_tabela, phi, padrao_atual, padroes)

# -----------------------------
# Execução FP-Growth
# -----------------------------
padroes_frequentes = {}
tabela_header = construir_fp_tree(transacoes, phi)
minerar_fp_growth(tabela_header, phi, [], padroes_frequentes)

print("\nITEMSETS FREQUENTES")
for itens, sup in sorted(padroes_frequentes.items(), key=lambda x: (len(x[0]), x[0])):
    print(set(itens), "->", sup)

# =========================================================
# GERAÇÃO DAS REGRAS DE ASSOCIAÇÃO
# =========================================================
print("\nREGRAS DE ASSOCIAÇÃO\n")

regras = []

for itemset in padroes_frequentes:
    if len(itemset) < 2:
        continue

    for i in range(1, len(itemset)):
        for antecedente in combinations(itemset, i):
            antecedente = frozenset(antecedente)
            consequente = itemset - antecedente

            suporte_itemset = padroes_frequentes[itemset]
            suporte_antecedente = padroes_frequentes[antecedente]
            suporte_consequente = padroes_frequentes[consequente]

            confianca = suporte_itemset / suporte_antecedente
            lift = confianca / (suporte_consequente / num_transacoes)

            if confianca >= confianca_minima:
                regras.append((
                    set(antecedente),
                    set(consequente),
                    suporte_itemset,
                    confianca,
                    lift
                ))

# -----------------------------
# Resultado final das regras
# -----------------------------
for a, c, s, conf, lift in regras:
    print(f"{a} -> {c} | suporte={s}, confiança={conf:.2f}, lift={lift:.2f}")
