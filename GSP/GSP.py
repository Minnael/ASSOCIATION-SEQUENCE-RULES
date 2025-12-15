base_dados = [
    [ {"pao"}, {"leite"}, {"manteiga"} ],     # Cliente 1
    [ {"pao"}, {"leite"} ],                   # Cliente 2
    [ {"pao"}, {"cerveja"} ],                 # Cliente 3
    [ {"leite"}, {"manteiga"} ],              # Cliente 4
    [ {"pao"}, {"leite"}, {"manteiga"} ]      # Cliente 5
]



# //////////////////////////////////////////////////////////////
# // 1. VERIFICA SE 'CANDIDATA' É SUBSEQUÊNCIA DE 'SEQUENCIA' //
# //////////////////////////////////////////////////////////////
def eh_subsequencia(candidata, sequencia):
    """
    Verifica se 'candidata' é subsequência de 'sequencia'
    """
    indice = 0

    for evento in sequencia:
        if candidata[indice].issubset(evento):
            indice += 1
            if indice == len(candidata):
                return True

    return False



# //////////////////////////////////////////////////////////
# // 2. CONTA O SUPORTE DE UMA CANDIDATA NA BASE DE DADOS //
# //////////////////////////////////////////////////////////
def contar_suporte(candidata, base_dados):
    suporte = 0

    for sequencia in base_dados:
        if eh_subsequencia(candidata, sequencia):
            suporte += 1

    return suporte



# /////////////////////////////////////////////////////////////////////////////
# // 3. GERA CANDIDATOS DE TAMANHO K+1 A PARTIR DAS SEQUÊNCIAS FREQUENTES LK //
# /////////////////////////////////////////////////////////////////////////////
def gerar_candidatos(Lk):
    """
    Gera candidatos de tamanho k+1 a partir das sequências frequentes Lk
    """
    candidatos = []

    for s1 in Lk:
        for s2 in Lk:
            if s1[1:] == s2[:-1]:
                nova_sequencia = s1 + [s2[-1]]

                if nova_sequencia not in candidatos:
                    candidatos.append(nova_sequencia)

    return candidatos



# //////////////////////////////////////////////////////////////////////////////
# // 4. ALGORITMO GSP PRINCIPAL PARA ENCONTRAR PADRÕES SEQUENCIAIS FREQUENTES //
# //////////////////////////////////////////////////////////////////////////////
def gsp(base_dados, suporte_minimo):
    # Coleta de todos os itens únicos
    itens = set()
    for sequencia in base_dados:
        for evento in sequencia:
            itens |= evento

    listas_frequentes = []
    L1 = []
    contagem_suporte = {}

    # Sequências de tamanho 1
    for item in itens:
        candidata = [ {item} ]
        sup = contar_suporte(candidata, base_dados)

        if sup >= suporte_minimo:
            L1.append(candidata)
            contagem_suporte[tuple(map(frozenset, candidata))] = sup

    listas_frequentes.append(L1)

    k = 0
    while listas_frequentes[k]:
        candidatos = gerar_candidatos(listas_frequentes[k])
        proximas_frequentes = []

        for candidata in candidatos:
            sup = contar_suporte(candidata, base_dados)

            if sup >= suporte_minimo:
                proximas_frequentes.append(candidata)
                contagem_suporte[tuple(map(frozenset, candidata))] = sup

        if not proximas_frequentes:
            break

        listas_frequentes.append(proximas_frequentes)
        k += 1

    return listas_frequentes, contagem_suporte



# ////////////////////////////////////////////////////////////////
# // 5. GERA REGRAS SEQUENCIAIS A PARTIR DOS PADRÕES FREQUENTES //
# ////////////////////////////////////////////////////////////////
def gerar_regras_sequenciais(listas_frequentes, contagem_suporte, confianca_minima):
    regras = []

    for nivel in listas_frequentes:
        for sequencia in nivel:
            if len(sequencia) < 2:
                continue

            suporte_total = contagem_suporte[tuple(map(frozenset, sequencia))]

            for i in range(1, len(sequencia)):
                antecedente = sequencia[:i]
                consequente = sequencia[i:]

                chave_antecedente = tuple(map(frozenset, antecedente))
                suporte_antecedente = contagem_suporte.get(chave_antecedente, 0)

                if suporte_antecedente > 0:
                    confianca = suporte_total / suporte_antecedente

                    if confianca >= confianca_minima:
                        regras.append((antecedente, consequente, confianca))

    return regras



suporte_minimo = 2      # 40% da base
confianca_minima = 0.6 # 60%

listas_frequentes, contagem_suporte = gsp(base_dados, suporte_minimo)
regras = gerar_regras_sequenciais(listas_frequentes, contagem_suporte, confianca_minima)


print("PADRÕES SEQUENCIAIS FREQUENTES:\n")

for nivel in listas_frequentes:
    for sequencia in nivel:
        suporte = contagem_suporte[tuple(map(frozenset, sequencia))]
        print(f"{sequencia}  | suporte = {suporte}")

print("\nREGRAS SEQUENCIAIS DESCOBERTAS:\n")

for antecedente, consequente, confianca in regras:
    print(f"{antecedente} ⇒ {consequente}  | confiança = {confianca:.2f}")
