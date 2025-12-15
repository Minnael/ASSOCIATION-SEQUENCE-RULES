from prefixspan import PrefixSpan

base_dados = [
    ["pao", "leite", "manteiga"],   # Cliente 1
    ["pao", "leite"],               # Cliente 2
    ["pao", "cerveja"],             # Cliente 3
    ["leite", "manteiga"],          # Cliente 4
    ["pao", "leite", "manteiga"]    # Cliente 5
]



# ///////////////////////////////////////////////
# // PASSO 1 — EXTRAÇÃO DOS PADRÕES FREQUENTES //
# ///////////////////////////////////////////////
ps = PrefixSpan(base_dados)
ps.minlen = 1
ps.maxlen = 10
min_suporte = 2
resultados = ps.frequent(min_suporte)

suporte_seq = {
    tuple(sequencia): suporte
    for suporte, sequencia in resultados
}



# //////////////////////////////////////////////
# // PASSO 2 — GERAÇÃO DAS REGRAS SEQUENCIAIS //
# // Regra: antecedente → consequente         //
# //////////////////////////////////////////////
regras = []

for sequencia, sup_seq in suporte_seq.items():
    if len(sequencia) < 2:
        continue

    for i in range(1, len(sequencia)):
        antecedente = sequencia[:i]
        consequente = sequencia[i:]

        sup_ant = suporte_seq.get(antecedente, 0)
        if sup_ant == 0:
            continue

        confianca = sup_seq / sup_ant

        regras.append(
            (antecedente, consequente, sup_seq, confianca)
        )



# //////////////////////////////////////////////////////////
# // PASSO 3 — FILTRAGEM DAS REGRAS POR CONFIANÇA MÍNIMA  //
# //////////////////////////////////////////////////////////
conf_min = 0.6
regras_filtradas = [
    r for r in regras if r[3] >= conf_min
]



# ///////////////////////////////////////////
# // PASSO 4 — APRESENTAÇÃO DOS RESULTADOS //
# ///////////////////////////////////////////
print("\nPADRÕES SEQUENCIAIS FREQUENTES:\n")
for seq, sup in suporte_seq.items():
    print(f"{seq} | suporte = {sup}")

print("\nREGRAS SEQUENCIAIS:\n")
for ant, cons, sup, conf in regras_filtradas:
    print(
        f"{ant} → {cons} | "
        f"suporte={sup} | "
        f"confiança={conf:.2f}"
    )
