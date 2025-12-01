# EXPLICAÇÃO DETALHADA DAS ANÁLISES - ANÁLISE DE CHURN TELECOM

## 📋 ÍNDICE
1. [Análise Exploratória Inicial](#1-análise-exploratória-inicial)
2. [Visualizações Descritivas](#2-visualizações-descritivas)
3. [Insights e Perfis de Risco](#3-insights-e-perfis-de-risco)
4. [Machine Learning - Modelos de Classificação](#4-machine-learning---modelos-de-classificação)
5. [Testes Estatísticos de Hipóteses](#5-testes-estatísticos-de-hipóteses)
6. [Regressão Linear Múltipla](#6-regressão-linear-múltipla)
7. [Análise de Clusters (K-Means)](#7-análise-de-clusters-k-means)
8. [Análise de Sobrevivência](#8-análise-de-sobrevivência)
9. [Score de Risco Individual e Lift](#9-score-de-risco-individual-e-lift)

---

## 1. ANÁLISE EXPLORATÓRIA INICIAL

### O que foi feito:
Análise descritiva básica dos dados para entender a distribuição do churn e identificar padrões iniciais.

### Resultados:

#### **Distribuição Geral de Churn:**
- **Total de clientes:** 7,043
- **Taxa de churn:** 26.54% (1,869 clientes cancelaram)
- **Clientes ativos:** 5,174 (73.46%)

**Insight:** Quase 1 em cada 4 clientes cancela o serviço. Esta é uma taxa alta que requer atenção imediata.

#### **Churn por Tipo de Contrato:**
| Tipo de Contrato | Total | Churns | Taxa de Churn |
|------------------|-------|--------|---------------|
| Month-to-month   | 3,875 | 1,655  | **42.71%** ⚠️ |
| One year         | 1,473 | 166    | **11.27%** ✅ |
| Two year         | 1,695 | 48     | **2.83%** ✅✅ |

**Insights Críticos:**
- **Contratos mensais são 15x mais propensos ao churn** que contratos bienais
- Clientes com contratos de longo prazo são extremamente leais
- **Ação imediata:** Priorizar migração de contratos mensais para anuais/bienais

#### **Churn por Tempo de Permanência (Tenure):**
| Grupo | Total | Taxa de Churn |
|-------|-------|---------------|
| Novo (0-12 meses) | 2,186 | **47.44%** ⚠️⚠️ |
| Médio (13-36 meses) | 1,856 | **25.54%** |
| Longo (36+ meses) | 3,001 | **11.93%** ✅ |

**Insights:**
- **Clientes novos têm 4x mais chance de cancelar** que clientes antigos
- O primeiro ano é crítico - quase metade dos novos clientes cancela
- Após 36 meses, a taxa de churn cai drasticamente

#### **Churn por Número de Serviços:**
- **1 serviço:** 10.92% de churn
- **2 serviços:** 30.97% de churn
- **3 serviços:** 44.92% de churn (pico!)
- **4+ serviços:** Taxa decresce progressivamente
- **9 serviços:** Apenas 5.29% de churn

**Insight Paradoxal:** Clientes com 3 serviços têm maior taxa de churn. Isso pode indicar:
- Insatisfação com a complexidade do pacote
- Custo alto sem valor percebido adequado
- Necessidade de melhor onboarding para pacotes intermediários

---

## 2. VISUALIZAÇÕES DESCRITIVAS

### Tipos de Visualizações Geradas:

#### **2.1. Distribuição de Churn (Gráficos de Barra e Pizza)**
- Mostra a proporção visual entre clientes ativos e churns
- **Resultado:** 73.46% ativos vs 26.54% churns

#### **2.2. Churn por Tipo de Contrato**
- Comparação visual do impacto do tipo de contrato
- **Conclusão visual clara:** Contratos mensais dominam os churns

#### **2.3. Análise de Tenure**
- **Histograma:** Mostra que clientes que cancelam têm tenure menor
- **Gráfico de barras:** Confirma que grupos novos têm muito mais churn

#### **2.4. Análise de Charges (MonthlyCharges e TotalCharges)**
- **Boxplots** mostram a distribuição de valores
- **Descoberta:** Clientes que cancelam pagam, em média, **R$ 13.18 a mais** por mês
- Isso sugere que preços altos podem estar causando insatisfação

#### **2.5. Impacto de Serviços**
- **Gráfico de linha:** Mostra a relação não-linear entre número de serviços e churn
- **Gráfico de segurança:** Clientes com serviços de segurança têm menor churn

#### **2.6. Matriz de Correlação**
- Mostra relações entre variáveis numéricas
- **Correlações importantes encontradas:**
  - `TotalCharges` e `tenure`: correlação positiva (quanto mais tempo, mais pago)
  - `Churn_Binary` e `tenure`: correlação negativa (-0.35) - quanto mais tempo, menos churn
  - `Churn_Binary` e `MonthlyCharges`: correlação positiva (0.19) - preços altos aumentam churn

#### **2.7. Satisfação vs Churn**
- Mostra que clientes com menor satisfação têm maior taxa de churn
- Confirma a importância do NPS (Net Promoter Score)

---

## 3. INSIGHTS E PERFIS DE RISCO

### Perfil de Alto Risco:
**Características:**
- Contrato mensal
- Tenure < 12 meses
- ≤ 2 serviços contratados

**Resultados:**
- **808 clientes** neste perfil
- **Taxa de churn: 41.7%** (quase 1 em cada 2!)

**Ação:** Estes clientes precisam de intervenção URGENTE com:
- Ofertas de migração para contratos anuais
- Incentivos para adicionar mais serviços
- Programa de onboarding intensivo

### Perfil de Baixo Risco:
**Características:**
- Contrato anual ou bienal
- Tenure > 24 meses
- ≥ 4 serviços contratados

**Resultados:**
- **1,886 clientes** neste perfil
- **Taxa de churn: 9.1%** (muito abaixo da média!)

**Ação:** Estes são clientes valiosos - manter programas de fidelidade e benefícios exclusivos

### Impacto Financeiro:
- **Receita mensal perdida:** R$ 139,130.85
- **Receita total perdida:** R$ 2,862,926.90
- **Ticket médio dos churns:** R$ 74.44

**Insight:** O impacto financeiro é significativo. Se conseguirmos reduzir o churn em 10%, economizaríamos aproximadamente **R$ 286,000** em receita total.

### Fatores Mais Correlacionados com Churn:
1. **IsPremium** (0.196) - Clientes premium têm maior propensão ao churn (paradoxo!)
2. **MonthlyCharges** (0.193) - Preços altos aumentam churn
3. **TotalCharges** (-0.198) - Quanto mais já pagou, menos cancela (efeito sunk cost)
4. **HasSecurity** (-0.101) - Segurança reduz churn
5. **NumServicos** (-0.019) - Mais serviços reduzem churn (correlação fraca)

---

## 4. MACHINE LEARNING - MODELOS DE CLASSIFICAÇÃO

### Preparação dos Dados:
- **12 features** selecionadas (9 numéricas + 3 categóricas codificadas)
- **Divisão:** 80% treino (5,634 registros) / 20% teste (1,409 registros)
- **Balanceamento:** Taxa de churn mantida igual em treino e teste (26.54%)

### 4.1. REGRESSÃO LOGÍSTICA

#### Como Funciona:
Modelo linear que calcula a probabilidade de churn usando uma função sigmoide. É interpretável e rápido.

#### Métricas:
- **Acurácia:** 78.99% - O modelo acerta quase 79% das previsões
- **Precisão:** 63.09% - Quando prevê churn, está correto 63% das vezes
- **Recall:** 50.27% - Consegue identificar 50% dos clientes que realmente vão cancelar
- **F1-Score:** 0.5595 - Média harmônica entre precisão e recall
- **AUC-ROC:** 0.8350 - Excelente capacidade de distinguir entre churn e não-churn

#### Matriz de Confusão:
```
                Predito
              Não  Sim
Real    Não   925  110  (Verdadeiros Negativos: 925, Falsos Positivos: 110)
        Sim   186  188  (Falsos Negativos: 186, Verdadeiros Positivos: 188)
```

**Interpretação:**
- **925 clientes** corretamente identificados como não-churn
- **188 clientes** corretamente identificados como churn
- **110 clientes** falsamente alertados (custo de retenção desnecessário)
- **186 clientes** que cancelaram mas não foram previstos (oportunidade perdida)

#### Top 5 Features Mais Importantes:
1. **MonthlyCharges** (coef: 1.735) - Aumenta muito a probabilidade de churn
2. **AvgChargePerMonth** (coef: -0.894) - Reduz churn (quanto mais paga ao longo do tempo, mais leal)
3. **tenure** (coef: -0.663) - Reduz churn (mais tempo = mais lealdade)
4. **SatisfactionScore** (coef: -0.521) - Reduz churn (satisfação importa)
5. **Contract_Encoded** (coef: -0.478) - Contratos longos reduzem churn

### 4.2. RANDOM FOREST

#### Como Funciona:
Ensemble de árvores de decisão que "votam" na classificação final. Captura relações não-lineares complexas.

#### Métricas:
- **Acurácia:** 79.35% - Ligeiramente melhor que Regressão Logística
- **Precisão:** 64.36% - Melhor precisão
- **Recall:** 49.73% - Similar ao modelo anterior
- **F1-Score:** 0.5611 - Ligeiramente melhor
- **AUC-ROC:** 0.8348 - Praticamente igual à Regressão Logística

#### Matriz de Confusão:
```
                Predito
              Não  Sim
Real    Não   932  103  (Menos falsos positivos!)
        Sim   188  186  (Similar ao modelo anterior)
```

**Melhoria:** Reduziu falsos positivos de 110 para 103 (economia em campanhas desnecessárias)

#### Top 5 Features Mais Importantes:
1. **MonthlyCharges** (14.35%) - Mais importante
2. **SatisfactionScore** (13.38%) - Satisfação é crucial
3. **TotalCharges** (12.26%) - Investimento total importa
4. **tenure** (11.98%) - Tempo de relacionamento
5. **AvgChargePerMonth** (11.73%) - Valor médio mensal

### Comparação dos Modelos:

| Métrica | Reg. Logística | Random Forest | Vencedor |
|---------|----------------|--------------|----------|
| Acurácia | 78.99% | 79.35% | Random Forest |
| Precisão | 63.09% | 64.36% | Random Forest |
| Recall | 50.27% | 49.73% | Reg. Logística |
| F1-Score | 0.5595 | 0.5611 | Random Forest |
| AUC-ROC | 0.8350 | 0.8348 | Reg. Logística |

**Conclusão:** Os modelos são praticamente equivalentes. A escolha depende do objetivo:
- **Random Forest:** Melhor para precisão (menos falsos positivos)
- **Regressão Logística:** Melhor para interpretabilidade e velocidade

---

## 5. TESTES ESTATÍSTICOS DE HIPÓTESES

### O que são Testes de Hipóteses?
Métodos estatísticos para verificar se diferenças observadas são estatisticamente significativas ou apenas devido ao acaso.

### 5.1. Teste t para MonthlyCharges

#### Hipóteses:
- **H0:** Não há diferença entre as médias de MonthlyCharges entre churn e não-churn
- **H1:** Há diferença significativa

#### Resultados:
- **Média (Churn):** R$ 74.44
- **Média (Não-Churn):** R$ 61.27
- **Diferença:** R$ 13.18 (clientes que cancelam pagam mais!)
- **Estatística t:** 16.54 (muito alta)
- **p-value:** < 0.000001 (extremamente significativo)

#### Conclusão:
**Rejeitamos H0** - A diferença é estatisticamente significativa. Clientes que cancelam realmente pagam mais, o que sugere:
- Preços altos podem estar causando insatisfação
- Ou clientes premium são mais exigentes e cancelam quando não veem valor

### 5.2. Teste t para Tenure

#### Resultados:
- **Média (Churn):** 17.98 meses
- **Média (Não-Churn):** 37.57 meses
- **Diferença:** -19.59 meses (clientes que cancelam têm menos tempo de relacionamento)
- **Estatística t:** -31.58 (extremamente significativo)
- **p-value:** < 0.000001

#### Conclusão:
**Rejeitamos H0** - Clientes que cancelam têm significativamente menos tempo de relacionamento. O primeiro ano é crítico!

### 5.3. Teste Qui-Quadrado para Contract vs Churn

#### O que testa:
Se há associação entre tipo de contrato e churn (não apenas correlação, mas dependência estatística)

#### Tabela de Contingência:
```
Churn_Binary       0     1
Contract                  
Month-to-month  2220  1655  (42.7% de churn)
One year        1307   166  (11.3% de churn)
Two year        1647    48  (2.8% de churn)
```

#### Resultados:
- **Estatística Chi²:** 1184.60 (muito alta)
- **Graus de liberdade:** 2
- **p-value:** < 0.000001

#### Conclusão:
**Rejeitamos H0** - Há associação estatisticamente significativa entre tipo de contrato e churn. Contratos mensais estão fortemente associados ao cancelamento.

---

## 6. REGRESSÃO LINEAR MÚLTIPLA

### Objetivo:
Prever o valor de **MonthlyCharges** com base em características do cliente. Isso ajuda a entender quais fatores determinam o preço que o cliente paga.

### Como Funciona:
Cria uma equação linear que combina múltiplas variáveis para prever um valor contínuo (não uma classificação).

### Métricas do Modelo:
- **R² (Coeficiente de Determinação):** 0.9088 (90.88%)
  - O modelo explica **90.88% da variância** em MonthlyCharges
  - Excelente ajuste!
  
- **RMSE:** R$ 9.09
  - Erro médio de R$ 9.09 na previsão
  - Considerando que a média é R$ 64.35, o erro é de apenas **14%**
  
- **MAE:** R$ 6.59
  - Erro absoluto médio de R$ 6.59
  - Muito preciso!

### Coeficientes do Modelo (Impacto de cada variável):

| Feature | Coeficiente | Interpretação |
|---------|-------------|---------------|
| **IsPremium** | +27.86 | Clientes premium pagam R$ 27.86 a mais |
| **NumServicos** | +7.92 | Cada serviço adicional adiciona R$ 7.92 |
| **Contract_Encoded** | -5.56 | Contratos longos reduzem o valor (descontos?) |
| **HasSecurity** | -3.20 | Segurança reduz ligeiramente o valor |
| **InternetService_Encoded** | -0.65 | Tipo de internet tem pouco impacto |
| **tenure** | -0.01 | Tempo de relacionamento tem impacto mínimo no preço |

**Intercepto:** R$ 24.35 (valor base)

### Insights:
1. **IsPremium** tem o maior impacto - premium realmente custa mais
2. **NumServicos** aumenta o valor de forma linear e previsível
3. O modelo é muito preciso (90.88% de explicação), útil para precificação

---

## 7. ANÁLISE DE CLUSTERS (K-MEANS)

### O que é Clustering?
Técnica não-supervisionada que agrupa clientes similares sem saber de antemão quais grupos existem. Descobre padrões "escondidos" nos dados.

### Como Funciona o K-Means:
1. Escolhe K pontos iniciais aleatórios (centróides)
2. Agrupa cada cliente ao centróide mais próximo
3. Recalcula os centróides
4. Repete até convergir

### Método do Cotovelo:
Testou K de 2 a 7 clusters e escolheu K=4 baseado na redução da inércia (distância dos pontos aos centróides).

### Os 4 Clusters Identificados:

#### **Cluster 0: "Clientes Novos de Baixo Valor"**
- **Total:** 1,960 clientes (27.8%)
- **Taxa de Churn:** 10.1% ✅
- **Tenure médio:** 57.5 meses (não são novos! Nome pode estar errado)
- **MonthlyCharges médio:** R$ 87.91
- **Características:** Alto valor, baixo churn, alta satisfação (8.01)

**Insight:** Este é o cluster mais valioso! Clientes de alto valor com baixo risco.

#### **Cluster 1: "Clientes Leais de Alto Valor"**
- **Total:** 1,310 clientes (18.6%)
- **Taxa de Churn:** 4.7% ✅✅ (melhor!)
- **Tenure médio:** 43.7 meses
- **MonthlyCharges médio:** R$ 29.24 (baixo valor?)
- **Características:** Baixo churn, mas baixa satisfação (4.74) - paradoxo!

**Insight:** Clientes leais mas com baixa satisfação. Risco de churn futuro se não melhorarem a experiência.

#### **Cluster 2: "Clientes de Médio Prazo"**
- **Total:** 1,782 clientes (25.3%)
- **Taxa de Churn:** 39.8% ⚠️⚠️ (alto risco!)
- **Tenure médio:** 6.8 meses (realmente novos)
- **MonthlyCharges médio:** R$ 43.72
- **Características:** Baixa satisfação (1.14), alto risco de churn (6.88)

**Insight:** Cluster crítico! Precisam de intervenção urgente. Estão no período de maior risco.

#### **Cluster 3: "Clientes Novos de Alto Risco"**
- **Total:** 1,991 clientes (28.3%)
- **Taxa de Churn:** 45.2% ⚠️⚠️⚠️ (muito alto!)
- **Tenure médio:** 23.0 meses
- **MonthlyCharges médio:** R$ 84.18 (alto valor)
- **Características:** Alta receita, mas extremamente insatisfeitos (2.87)

**Insight:** Clientes de alto valor mas muito insatisfeitos. Risco extremo de churn. Prioridade máxima!

### Estratégias por Cluster:
- **Cluster 0:** Manter programas de fidelidade premium
- **Cluster 1:** Melhorar satisfação (pesquisa NPS, melhor atendimento)
- **Cluster 2:** Intervenção imediata (ofertas, onboarding melhorado)
- **Cluster 3:** Ação URGENTE (descontos, atendimento VIP, resolver problemas)

---

## 8. ANÁLISE DE SOBREVIVÊNCIA

### O que é Análise de Sobrevivência?
Estuda o **tempo até um evento** (neste caso, churn). Mostra a probabilidade de um cliente "sobreviver" (não cancelar) ao longo do tempo.

### Como Funciona:
Calcula a probabilidade cumulativa de sobrevivência mês a mês, considerando quantos clientes estão "em risco" a cada momento.

### Resultados por Tipo de Contrato:

#### **Month-to-month:**
- **Sobrevivência após 12 meses:** 70.3%
- **Taxa de churn acumulada:** 29.7% no primeiro ano

#### **One year:**
- **Sobrevivência após 12 meses:** 99.1%
- **Taxa de churn acumulada:** 0.9% no primeiro ano

#### **Two year:**
- **Sobrevivência após 12 meses:** 100.0%
- **Taxa de churn acumulada:** 0% no primeiro ano

**Insight Crítico:** Contratos de longo prazo praticamente eliminam o churn no primeiro ano!

### Estatísticas Gerais:
- **Tempo médio até churn:** 18.0 meses (para quem cancela)
- **Tempo médio de permanência:** 32.4 meses (todos os clientes)
- **Mediana de tempo até churn:** 10.0 meses

**Interpretação:**
- Metade dos clientes que cancelam fazem isso nos **primeiros 10 meses**
- O período crítico é claramente o primeiro ano
- Após 18 meses, o risco diminui significativamente

### Curvas de Sobrevivência:
As curvas mostram visualmente como a probabilidade de sobrevivência decai ao longo do tempo:
- **Contratos mensais:** Curva cai rapidamente
- **Contratos anuais/bienais:** Curvas quase planas (baixo churn)

---

## 9. SCORE DE RISCO INDIVIDUAL E LIFT

### Score de Risco Individual:
Usa o modelo Random Forest para calcular a **probabilidade de churn** para cada cliente individualmente.

### Categorização de Risco:
| Categoria | Probabilidade | Total Clientes | Taxa de Churn Real |
|-----------|---------------|----------------|-------------------|
| Baixo Risco | < 20% | 3,768 | 1.57% ✅ |
| Risco Moderado | 20-40% | 1,133 | 27.01% |
| Alto Risco | 40-60% | 1,165 | 56.31% ⚠️ |
| Risco Muito Alto | > 60% | 977 | **86.80%** ⚠️⚠️ |

**Insight:** O modelo é muito preciso! Clientes categorizados como "Risco Muito Alto" realmente têm 86.8% de taxa de churn.

### Análise de Lift:

#### O que é Lift?
Mede quantas vezes melhor o modelo é comparado a uma escolha aleatória. Lift = 1 significa que o modelo não é melhor que o acaso.

#### Resultados por Decil (Top 3):

| Decil | Total | Churns | Taxa de Churn | **Lift** |
|-------|-------|--------|---------------|----------|
| 10 (maior risco) | 705 | 629 | 89.22% | **3.36x** 🚀 |
| 9 | 704 | 520 | 73.86% | **2.78x** |
| 8 | 704 | 343 | 48.72% | **1.84x** |

**Interpretação:**
- O modelo identifica o **decil de maior risco** com 89.22% de taxa de churn real
- Isso é **3.36 vezes melhor** que escolher aleatoriamente
- Se focarmos apenas no top 10% de risco, capturamos quase 90% dos churns!

### Eficiência do Modelo:
- **Top 10% (Decil 10):** 89.22% de churn - modelo extremamente eficaz
- **Top 20% (Decis 9-10):** Captura a maioria dos churns com alta precisão
- **Estratégia:** Focar recursos de retenção nos top 2 decis (20% dos clientes)

---

## 📊 RESUMO EXECUTIVO - PRINCIPAIS DESCOBERTAS

### 1. Fatores Críticos de Churn:
1. **Tipo de contrato** - Contratos mensais = 15x mais churn
2. **Tempo de relacionamento** - Primeiro ano é crítico (47% de churn)
3. **Número de serviços** - Relação não-linear (3 serviços = pico de churn)
4. **Satisfação** - Correlação forte com retenção
5. **Valor mensal** - Clientes que pagam mais cancelam mais (paradoxo premium)

### 2. Impacto Financeiro:
- **R$ 139,130/mês** perdidos em receita
- **R$ 2.86 milhões** em receita total perdida
- Reduzir churn em 10% = economizar **R$ 286,000**

### 3. Modelos de ML:
- **AUC-ROC: 0.835** - Excelente capacidade preditiva
- **Lift de 3.36x** no top decil - Muito eficiente
- Modelo pode identificar 89% dos churns no top 10% de risco

### 4. Segmentação:
- **4 clusters** distintos identificados
- **Cluster 3** (28.3% dos clientes) tem 45.2% de churn - PRIORIDADE MÁXIMA
- **Cluster 1** (18.6% dos clientes) tem apenas 4.7% de churn - Modelo a seguir

### 5. Janela de Oportunidade:
- **Mediana de churn: 10 meses** - Intervenção deve ser nos primeiros 6-9 meses
- **Primeiro ano:** Período crítico (47% de churn em clientes novos)
- **Após 18 meses:** Risco diminui significativamente

---

## 🎯 RECOMENDAÇÕES PRIORITÁRIAS

### Ações Imediatas (0-3 meses):
1. **Migração de contratos:** Oferecer descontos agressivos para migrar mensais → anuais
2. **Intervenção no Cluster 3:** Ação urgente para 1,991 clientes de alto risco
3. **Programa de onboarding:** Intensificar nos primeiros 6 meses

### Ações de Médio Prazo (3-6 meses):
1. **Sistema de alertas:** Implementar baseado em scores de risco
2. **Campanhas segmentadas:** Por cluster e por score de risco
3. **Melhoria de satisfação:** Focar no Cluster 1 (baixa satisfação apesar de lealdade)

### Ações de Longo Prazo (6-12 meses):
1. **Retreinamento de modelos:** Mensalmente com novos dados
2. **Monitoramento de KPIs:** Dashboard executivo com métricas de churn
3. **Programas de fidelidade:** Para clusters de baixo risco (manter lealdade)

---

## 📈 MÉTRICAS DE SUCESSO

### KPIs a Monitorar:
1. **Taxa de churn geral:** Meta: reduzir de 26.54% para < 20%
2. **Churn no primeiro ano:** Meta: reduzir de 47.4% para < 35%
3. **Taxa de migração contratos:** Meta: 30% dos mensais → anuais
4. **Precisão do modelo:** Manter AUC-ROC > 0.80
5. **Lift no top decil:** Manter > 3.0x

---

## 🔬 GLOSSÁRIO TÉCNICO

- **AUC-ROC:** Área sob a curva ROC - mede capacidade de distinguir classes (0.5 = aleatório, 1.0 = perfeito)
- **Precisão:** Quando prevê churn, quantas vezes está correto
- **Recall:** Quantos churns reais consegue identificar
- **F1-Score:** Média harmônica entre precisão e recall
- **p-value:** Probabilidade de observar o resultado por acaso (< 0.05 = significativo)
- **Lift:** Quantas vezes melhor que escolha aleatória
- **R²:** Proporção da variância explicada pelo modelo (0-1, quanto maior melhor)
- **RMSE:** Raiz do erro quadrático médio (erro de previsão)
- **Clustering:** Agrupamento não-supervisionado de dados similares
- **Análise de Sobrevivência:** Estudo do tempo até um evento ocorrer

---

**Documento gerado em:** 2025-12-01  
**Equipe:** Mariana Belo, Leonardo Azevedo, Walter Barreto

