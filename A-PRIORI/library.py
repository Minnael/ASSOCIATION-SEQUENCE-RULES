import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


# ///////////////////////
# // DATASET UTILIZADO //
# ///////////////////////
transacoes = [
    {"tomate", "cerveja", "arroz", "frango"},
    {"tomate", "cerveja", "arroz"},
    {"tomate", "cerveja", "arroz"},
    {"tomate", "pera"},
    {"mamadeira", "cerveja", "arroz", "frango"},
    {"mamadeira", "cerveja", "arroz"},
    {"mamadeira", "cerveja"},
    {"mamadeira", "pera"},
]



# ////////////////////////////////////////////////////////////////
# // TRANSFORMAR PARA FORMATO ONE-HOT (NECESSÁRIO PARA MLXTEND) //
# ////////////////////////////////////////////////////////////////
te = TransactionEncoder()
te_ary = te.fit(transacoes).transform(transacoes)
df = pd.DataFrame(te_ary, columns=te.columns_)

print("\n=== DataFrame One-Hot ===")
print(df)





# /////////////////////
# // APLICAR APRIORI //
# /////////////////////
itemsets_frequentes = apriori(
    df,
    min_support=0.375,  
    use_colnames=True
)

print("\n=== ITEMSETS FREQUENTES (MLXTEND) ===")
print(itemsets_frequentes)





# ////////////////////////////////////////////////////////
# // AGRUPAR E PRINTAR EM FORMATO L1, L2, L3...          //
# ////////////////////////////////////////////////////////
print("\n\n=========== ITEMSETS POR NÍVEL (L1, L2, L3...) ===========")

# adicionar coluna tamanho
itemsets_frequentes["tamanho"] = itemsets_frequentes["itemsets"].apply(len)

max_k = itemsets_frequentes["tamanho"].max()

for k in range(1, max_k + 1):
    nivel = itemsets_frequentes[itemsets_frequentes["tamanho"] == k]
    print(f"\n--- L{k} ---")
    
    for _, row in nivel.iterrows():
        itens = set(row["itemsets"])
        sup = row["support"]
        print(f"{itens} | suporte = {sup:.2f}")





# ////////////////////////////////
# // GERAR REGRAS DE ASSOCIAÇÃO //
# ////////////////////////////////
regras = association_rules(
    itemsets_frequentes,
    metric="confidence",
    min_threshold=0.60
)

print("\n=== REGRAS DE ASSOCIAÇÃO ===")
print(regras[["antecedents", "consequents", "support", "confidence", "lift"]])
