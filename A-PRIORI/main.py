from apriori import apriori, gerar_regras, calcular_suporte

transacoes = [
    {"pão", "leite", "manteiga"},
    {"pão", "leite"},
    {"leite", "cerveja", "frutas"},
    {"pão", "cerveja"},
    {"pão", "leite", "cerveja"},
    {"leite", "frutas"},
    {"pão", "leite", "manteiga", "cerveja"},
    {"pão", "manteiga"},
]

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

min_support = 0.375
min_confidence = 0.6

itemsets = apriori(transacoes, min_support)

print("=== ITEMSETS FREQUENTES ===")
nivel_atual = 1
for nivel in itemsets:
    print(f"\n--- L{nivel_atual} ---")
    for itemset in nivel:
        sup = calcular_suporte(itemset, transacoes)
        print(f"{set(itemset)} | suporte={sup:.2f}")
    nivel_atual += 1

regras = gerar_regras(itemsets, transacoes, min_confidence)

print("\n=== REGRAS DE ASSOCIAÇÃO ===")
for A, B, conf, sup in regras:
    print(f"{set(A)} → {set(B)} | confiança={conf:.2f} | suporte={sup:.2f}")