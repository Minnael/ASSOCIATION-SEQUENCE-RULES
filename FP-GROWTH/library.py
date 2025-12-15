import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules


# /////////////////////////
# // BASE DE TRANSAÇÕES  //
# /////////////////////////
transacoes = [
    ['a', 'b'],
    ['b', 'c', 'd'],
    ['a', 'c', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'b', 'c'],
    ['a', 'b', 'c', 'd'],
    ['a'],
    ['a', 'b', 'c'],
    ['a', 'b', 'd'],
    ['b', 'c', 'e']
]

phi = 2 
num_transacoes = len(transacoes)
confianca_minima = 0.6



# ////////////////////////////////////////////////////////////////
# // TRANSFORMAR PARA FORMATO ONE-HOT (NECESSÁRIO PARA MLXTEND) //
# ////////////////////////////////////////////////////////////////
itens = sorted({item for t in transacoes for item in t})
matriz = []

for t in transacoes:
    matriz.append({item: (item in t) for item in itens})

df = pd.DataFrame(matriz)



# ////////////////////////////
# // EXECUÇÃO DO FP-GROWTH  //
# ////////////////////////////
itemsets = fpgrowth(
    df,
    min_support=phi / num_transacoes,
    use_colnames=True
)

print("ITEMSETS FREQUENTES — FP-GROWTH (mlxtend)\n")
for _, linha in itemsets.iterrows():
    print(set(linha['itemsets']), "->", int(linha['support'] * num_transacoes))



# ///////////////////////////////////////////////////
# // GERAÇÃO DAS REGRAS DE ASSOCIAÇÃO (BIBLIOTECA) //
# ///////////////////////////////////////////////////
regras = association_rules(
    itemsets,
    metric="confidence",
    min_threshold=confianca_minima
)

print("\nREGRAS DE ASSOCIAÇÃO\n")
for _, r in regras.iterrows():
    antecedente = set(r['antecedents'])
    consequente = set(r['consequents'])
    suporte = int(r['support'] * num_transacoes)
    confianca = r['confidence']
    lift = r['lift']

    print(
        f"{antecedente} -> {consequente} | "
        f"suporte={suporte}, confiança={confianca:.2f}, lift={lift:.2f}"
    )
