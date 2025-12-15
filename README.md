# Algoritmos de Mineração de Dados

Este repositório contém implementações de algoritmos clássicos de mineração de dados para descoberta de padrões frequentes e regras de associação.

---

## 📚 Índice

1. [Apriori](#apriori)
2. [FP-Growth](#fp-growth)
3. [GSP - Generalized Sequential Pattern](#gsp)
4. [PrefixSpan](#prefixspan)

---

## 🔍 Apriori

### Descrição
O **Apriori** é um algoritmo clássico para mineração de regras de associação em bases de dados transacionais. Ele identifica conjuntos de itens frequentes e gera regras de associação baseadas em suporte e confiança mínimos.

### Fórmulas Matemáticas

#### Suporte
Mede a frequência de um itemset no dataset:

$$\text{Suporte}(X) = \frac{\text{Número de transações contendo } X}{\text{Total de transações}}$$

#### Confiança
Mede a força da regra $X \rightarrow Y$:

$$\text{Confiança}(X \rightarrow Y) = \frac{\text{Suporte}(X \cup Y)}{\text{Suporte}(X)}$$

#### Lift
Mede a independência entre X e Y:

$$\text{Lift}(X \rightarrow Y) = \frac{\text{Confiança}(X \rightarrow Y)}{\text{Suporte}(Y)}$$

- **Lift > 1**: X e Y são positivamente correlacionados
- **Lift = 1**: X e Y são independentes
- **Lift < 1**: X e Y são negativamente correlacionados

### Funcionamento

1. **L1**: Encontra itemsets de tamanho 1 que atendem ao suporte mínimo
2. **Geração de Candidatos**: Combina itemsets de tamanho k para gerar candidatos de tamanho k+1
3. **Poda**: Remove candidatos que não atendem ao suporte mínimo
4. **Iteração**: Repete até não haver mais itemsets frequentes
5. **Regras**: Gera regras de associação a partir dos itemsets frequentes

### Resultados (Dataset de Exemplo)

**Dataset**: 8 transações com itens {tomate, cerveja, arroz, frango, mamadeira, pera}

**Parâmetros**:
- Suporte mínimo: 0.375 (37.5%)
- Confiança mínima: 0.60 (60%)

**Itemsets Frequentes**:
- **L1**: {cerveja}, {arroz}, {tomate}, {mamadeira}
- **L2**: {cerveja, arroz}, {tomate, cerveja}, {tomate, arroz}
- **L3**: {tomate, cerveja, arroz}

**Exemplos de Regras**:
- {cerveja} → {arroz} | confiança=0.86 | suporte=0.50
- {tomate} → {cerveja, arroz} | confiança=0.75 | suporte=0.375

---

## 🌳 FP-Growth

### Descrição
O **FP-Growth** (Frequent Pattern Growth) é um algoritmo mais eficiente que o Apriori, pois evita a geração de candidatos. Utiliza uma estrutura de dados compacta chamada **FP-Tree** para armazenar informações sobre transações frequentes.

### Fórmulas Matemáticas

Utiliza as mesmas métricas do Apriori:
- **Suporte**: $\text{Suporte}(X) = \frac{\text{count}(X)}{N}$
- **Confiança**: $\text{Confiança}(X \rightarrow Y) = \frac{\text{Suporte}(X \cup Y)}{\text{Suporte}(X)}$
- **Lift**: $\text{Lift}(X \rightarrow Y) = \frac{\text{Confiança}(X \rightarrow Y)}{\text{Suporte}(Y)}$

### Funcionamento

1. **Primeira Varredura**: Conta a frequência de cada item
2. **Ordenação**: Ordena itens por frequência decrescente
3. **Construção da FP-Tree**: 
   - Cria uma árvore compacta com nós compartilhados
   - Mantém uma tabela de cabeçalhos (header table) para acesso rápido
4. **Mineração Recursiva**:
   - Para cada item, constrói uma base de padrões condicionais
   - Gera FP-Tree condicional
   - Extrai padrões frequentes recursivamente

### Vantagens sobre Apriori
- Apenas 2 varreduras no dataset
- Não gera candidatos explicitamente
- Estrutura compacta em memória
- Mais eficiente para datasets grandes

### Resultados (Dataset de Exemplo)

**Dataset**: 10 transações com itens {a, b, c, d, e}

**Parâmetros**:
- Suporte mínimo: 2 transações
- Confiança mínima: 0.60

**Itemsets Frequentes Encontrados**:
- Tamanho 1: {a}→9, {b}→7, {c}→6, {d}→6, {e}→3
- Tamanho 2: {a,b}→6, {a,c}→5, {a,d}→5, {b,c}→5, {b,d}→4, {c,d}→3
- Tamanho 3: {a,b,c}→4, {a,b,d}→3, {a,c,d}→2, {b,c,d}→2
- Tamanho 4: {a,b,c,d}→2

**Exemplos de Regras**:
- {b} → {a} | suporte=6, confiança=0.86, lift=0.95
- {c,d} → {a} | suporte=2, confiança=0.67, lift=0.74

---

## 📊 GSP (Generalized Sequential Pattern)

### Descrição
O **GSP** é um algoritmo para mineração de padrões sequenciais. Diferente do Apriori, que trabalha com conjuntos (sem ordem), o GSP considera a **ordem temporal** dos eventos, identificando sequências frequentes.

### Conceitos

- **Sequência**: Lista ordenada de eventos
- **Evento (itemset)**: Conjunto de itens que ocorrem simultaneamente
- **Subsequência**: Uma sequência S é subsequência de T se todos os elementos de S aparecem em T na mesma ordem

**Exemplo**: 
- Sequência: `<{pão}, {leite}, {manteiga}>`
- `<{pão}, {manteiga}>` é subsequência válida
- `<{manteiga}, {pão}>` NÃO é subsequência (ordem invertida)

### Fórmulas Matemáticas

#### Suporte de Sequência
$$\text{Suporte}(S) = \frac{\text{Número de clientes que contêm a sequência } S}{\text{Total de clientes}}$$

#### Confiança de Regra Sequencial
Para uma regra $S_1 \Rightarrow S_2$:

$$\text{Confiança}(S_1 \Rightarrow S_2) = \frac{\text{Suporte}(S_1 \cdot S_2)}{\text{Suporte}(S_1)}$$

onde $S_1 \cdot S_2$ representa a concatenação das sequências.

### Funcionamento

1. **Fase 1**: Encontra sequências de tamanho 1 frequentes
2. **Geração de Candidatos**: Combina sequências de tamanho k para gerar k+1
   - **Join**: Junta duas sequências se compartilham k-1 elementos
3. **Poda**: Remove candidatos que não atingem suporte mínimo
4. **Iteração**: Repete até não haver mais padrões frequentes
5. **Regras**: Gera regras sequenciais com base na confiança

### Resultados (Dataset de Exemplo)

**Dataset**: 5 clientes com sequências de compras

```
Cliente 1: <{pão}, {leite}, {manteiga}>
Cliente 2: <{pão}, {leite}>
Cliente 3: <{pão}, {cerveja}>
Cliente 4: <{leite}, {manteiga}>
Cliente 5: <{pão}, {leite}, {manteiga}>
```

**Parâmetros**:
- Suporte mínimo: 2 (40% dos clientes)
- Confiança mínima: 0.60

**Padrões Sequenciais Frequentes**:
- Tamanho 1: `<{pão}>`, `<{leite}>`, `<{manteiga}>`
- Tamanho 2: `<{pão}, {leite}>`, `<{leite}, {manteiga}>`
- Tamanho 3: `<{pão}, {leite}, {manteiga}>`

**Regras Sequenciais**:
- `<{pão}>` ⇒ `<{leite}>` | confiança=0.75
- `<{leite}>` ⇒ `<{manteiga}>` | confiança=0.67
- `<{pão}, {leite}>` ⇒ `<{manteiga}>` | confiança=0.67

---

## 🔗 PrefixSpan

### Descrição
O **PrefixSpan** (Prefix-Projected Sequential Pattern Mining) é um algoritmo mais eficiente que o GSP para mineração de padrões sequenciais. Ele usa uma abordagem de **crescimento de padrão** e **projeção de banco de dados**, evitando a geração de candidatos.

### Fórmulas Matemáticas

Utiliza as mesmas métricas do GSP:

#### Suporte
$$\text{Suporte}(S) = \frac{|\{sid \in D \mid S \subseteq sid\}|}{|D|}$$

onde $D$ é o conjunto de todas as sequências e $S \subseteq sid$ indica que S é subsequência de sid.

#### Confiança
$$\text{Confiança}(\alpha \Rightarrow \beta) = \frac{\text{Suporte}(\alpha \cdot \beta)}{\text{Suporte}(\alpha)}$$

### Funcionamento

1. **Busca em Profundidade**: Explora o espaço de busca em profundidade
2. **Divisão e Conquista**: 
   - Divide o problema em subproblemas menores
   - Para cada prefixo frequente, cria um banco de dados projetado
3. **Projeção**: 
   - Projeta o banco de dados com base no prefixo atual
   - Reduz o tamanho do problema progressivamente
4. **Recursão**: Minera padrões nos bancos projetados

### Vantagens sobre GSP
- **Não gera candidatos**: Evita explosão combinatória
- **Busca em profundidade**: Mais eficiente em memória
- **Projeção de DB**: Reduz progressivamente o tamanho do problema
- **Mais rápido**: Especialmente para sequências longas

### Resultados (Dataset de Exemplo)

**Dataset**: 5 clientes com sequências

```
Cliente 1: ["pao", "leite", "manteiga"]
Cliente 2: ["pao", "leite"]
Cliente 3: ["pao", "cerveja"]
Cliente 4: ["leite", "manteiga"]
Cliente 5: ["pao", "leite", "manteiga"]
```

**Parâmetros**:
- Suporte mínimo: 2
- Confiança mínima: 0.60
- minlen: 1, maxlen: 10

**Padrões Frequentes**:
- ('pao',) | suporte=4
- ('leite',) | suporte=4
- ('manteiga',) | suporte=3
- ('pao', 'leite') | suporte=3
- ('leite', 'manteiga') | suporte=3
- ('pao', 'leite', 'manteiga') | suporte=2

**Regras Sequenciais**:
- ('pao',) → ('leite',) | suporte=3 | confiança=0.75
- ('leite',) → ('manteiga',) | suporte=3 | confiança=0.75
- ('pao', 'leite') → ('manteiga',) | suporte=2 | confiança=0.67

---

## 📊 Comparação dos Algoritmos

| Característica | Apriori | FP-Growth | GSP | PrefixSpan |
|---------------|---------|-----------|-----|------------|
| **Tipo** | Itemsets | Itemsets | Sequencial | Sequencial |
| **Gera Candidatos** | Sim | Não | Sim | Não |
| **Estrutura** | Lista | FP-Tree | Lista | Projeção |
| **Varreduras DB** | Múltiplas | 2 | Múltiplas | 1 + Projeções |
| **Ordem Importa** | Não | Não | Sim | Sim |
| **Eficiência** | Baixa | Alta | Média | Alta |
| **Memória** | Baixa | Média | Baixa | Baixa |

### Quando Usar Cada Algoritmo?

- **Apriori**: Datasets pequenos, didático, quando se quer entender o funcionamento básico
- **FP-Growth**: Datasets grandes, quando não há ordem temporal, melhor performance
- **GSP**: Quando a ordem dos eventos é importante, análise de comportamento sequencial
- **PrefixSpan**: Grandes volumes de dados sequenciais, melhor performance que GSP

---

## 🛠️ Estrutura do Repositório

```
CODES/
├── A-PRIORI/
│   ├── apriori.py        # Implementação manual
│   ├── library.py        # Usando MLxtend
│   └── main.py           # Execução principal
├── FP-GROWTH/
│   ├── fp-growth.py      # Implementação manual
│   └── library.py        # Usando MLxtend
├── GSP/
│   └── GSP.py            # Implementação completa
├── PREFIXSPAN/
│   └── library.py        # Usando biblioteca prefixspan
└── README.md             # Este arquivo
```

---

## 📦 Dependências

```bash
pip install pandas
pip install mlxtend
pip install prefixspan
```

---

## 🚀 Como Executar

### Apriori
```bash
cd A-PRIORI
python main.py
# ou
python library.py
```

### FP-Growth
```bash
cd FP-GROWTH
python fp-growth.py
# ou
python library.py
```

### GSP
```bash
cd GSP
python GSP.py
```

### PrefixSpan
```bash
cd PREFIXSPAN
python library.py
```

---

## 📖 Referências

- Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules. *VLDB*.
- Han, J., Pei, J., & Yin, Y. (2000). Mining frequent patterns without candidate generation. *SIGMOD*.
- Srikant, R., & Agrawal, R. (1996). Mining sequential patterns: Generalizations and performance improvements. *EDBT*.
- Pei, J., et al. (2001). PrefixSpan: Mining sequential patterns efficiently by prefix-projected pattern growth. *ICDE*.

---

## 👨‍🎓 Contexto Acadêmico

Este repositório foi desenvolvido como parte de estudos de Mestrado em Ciência da Computação, focando em técnicas de Mineração de Dados e Descoberta de Conhecimento em Bases de Dados (KDD).

---

## 📝 Licença

Material acadêmico para fins educacionais.
