# Documento de Arquitetura - Pipeline de Big Data
## Análise de Churn Telecom

**Equipe:** Leonardo Azevedo, Walter Barreto, Mariana Belo  
**Data:** 13/10/2024  
**Disciplina:** Fundamentos de Big Data  

---

## 1. Visão Geral do Projeto

### 1.1 Objetivo
Desenvolver uma solução completa de análise de churn para uma empresa de telecomunicações, utilizando um pipeline de Big Data que processa dados desde a ingestão até a geração de insights estratégicos.

### 1.2 Problema de Negócio
A empresa enfrenta uma taxa de churn de 26.54%, resultando em perda mensal de R$ 139.130,85 em receita. O objetivo é identificar padrões e fatores que levam ao cancelamento de serviços para implementar estratégias de retenção.

---

## 2. Arquitetura do Pipeline

### 2.1 Diagrama da Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FONTES DE     │    │    INGESTÃO     │    │   ARMAZENAMENTO │
│     DADOS       │───▶│   (Bronze)      │───▶│   ESTRUTURADO   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       ▼
         │                       │              ┌─────────────────┐
         │                       │              │   TRANSFORMAÇÃO │
         │                       │              │    (Silver)     │
         │                       │              └─────────────────┘
         │                       │                       │
         │                       │                       ▼
         │                       │              ┌─────────────────┐
         │                       │              │   CARREGAMENTO  │
         │                       │              │     (Gold)      │
         │                       │              └─────────────────┘
         │                       │                       │
         │                       │                       ▼
         │                       │              ┌─────────────────┐
         │                       │              │   ANÁLISE E     │
         │                       │              │ VISUALIZAÇÃO    │
         │                       │              └─────────────────┘
```

### 2.2 Arquitetura Medallion (Bronze-Silver-Gold)

```
/dados/
├── bronze/          # Dados brutos (raw data)
│   ├── telco_churn_raw.csv
│   └── relatorio_ingestao.txt
├── silver/          # Dados transformados e limpos
│   ├── telco_churn_transformed.csv
│   ├── telco_churn_transformed.parquet
│   └── relatorio_transformacao.txt
└── gold/            # Dados prontos para análise
    ├── metricas_por_contrato.csv
    ├── churn_por_segmento.csv
    ├── perfil_alto_risco.csv
    ├── correlacoes_churn.csv
    ├── viz_*.png (7 visualizações)
    ├── dashboard_final.png
    └── relatorio_final.txt
```

---

## 3. Detalhamento das Etapas do Pipeline

### 3.1 Fontes de Dados (Data Sources)

**Descrição:** Dataset público de churn de telecomunicações  
**Tipo:** Dados estruturados (CSV)  
**Origem:** Kaggle/IBM  
**Características:**
- 7.043 registros de clientes
- 23 colunas (demográficas, contratuais, de serviços)
- Dados históricos de 2019-2020

**Campos principais:**
- `customerID`: Identificador único
- `Churn`: Variável alvo (Yes/No)
- `tenure`: Tempo de permanência (meses)
- `MonthlyCharges`: Cobrança mensal
- `Contract`: Tipo de contrato
- Serviços contratados (PhoneService, InternetService, etc.)

### 3.2 Ingestão (Ingestion)

**Tipo:** Batch processing  
**Ferramentas utilizadas:**
- `pandas.read_csv()`: Leitura do arquivo CSV
- `urllib.request`: Download automático do dataset
- Validação de integridade dos dados

**Processo implementado:**
1. Verificação de arquivos locais existentes
2. Download automático do GitHub (fallback)
3. Validação de integridade dos dados
4. Adição de metadados de ingestão
5. Salvamento na camada Bronze

**Qualidade dos dados:**
- ✅ 7.043 registros ingeridos
- ✅ 23 colunas processadas
- ✅ 0 duplicatas encontradas
- ✅ Taxa de churn: 26.54%

### 3.3 Transformação (Transformation)

**Ferramentas utilizadas:**
- **Pandas**: Manipulação e limpeza de dados
- **NumPy**: Operações vetorizadas
- **PyArrow**: Formato Parquet para eficiência
- **Scikit-learn**: Normalização (MinMaxScaler)

**Processos implementados:**

#### 3.3.1 Limpeza de Dados
- Conversão de `TotalCharges` para numérico
- Tratamento de valores ausentes (11 registros)
- Remoção de duplicatas
- Padronização de valores categóricos

#### 3.3.2 Engenharia de Features
**10 novas features criadas:**
1. `Churn_Binary`: Conversão binária da variável alvo
2. `AvgChargePerMonth`: Valor médio por mês
3. `TenureGroup`: Categorização (Novo/Médio/Longo)
4. `IsPremium`: Flag de cliente premium
5. `NumServicos`: Total de serviços contratados
6. `HasSecurity`: Flag de serviços de segurança
7. `SatisfactionScore`: Score de satisfação (0-10)
8. `ChurnRiskScore`: Score de risco (0-9)
9. `MonthlyCharges_Normalized`: Normalização 0-1
10. `TotalCharges_Normalized`: Normalização 0-1

#### 3.3.3 Agregações Estatísticas
- Métricas por tipo de contrato
- Estatísticas por grupo de tenure
- Correlações entre variáveis

**Resultados:**
- ✅ 7.043 registros processados
- ✅ 33 colunas (10 novas features)
- ✅ 0 valores ausentes
- ✅ Redução de 80.7% no tamanho (Parquet vs CSV)

### 3.4 Carregamento (Loading)

**Formatos de saída:**
- **CSV**: Compatibilidade e portabilidade
- **Parquet**: Eficiência e compressão
- **Datasets agregados**: Análise otimizada

**Datasets Gold criados:**
1. `metricas_por_contrato.csv`: KPIs por tipo de contrato
2. `churn_por_segmento.csv`: Análise de segmentos
3. `perfil_alto_risco.csv`: Características de clientes em risco
4. `correlacoes_churn.csv`: Features mais correlacionadas

### 3.5 Destino (Destination)

**Ferramentas de visualização:**
- **Matplotlib**: Gráficos básicos
- **Seaborn**: Visualizações estatísticas
- **Pandas**: Análise exploratória

**Entregáveis gerados:**
- 7 visualizações PNG de alta qualidade
- Dashboard executivo consolidado
- Relatório final com insights estratégicos

---

## 4. Tecnologias Utilizadas

### 4.1 Tecnologias Implementadas

| Categoria | Tecnologia | Justificativa |
|-----------|------------|---------------|
| **Processamento** | Python 3.x | Linguagem padrão para Data Science |
| **Manipulação** | Pandas | Biblioteca principal para análise de dados |
| **Computação** | NumPy | Operações vetorizadas eficientes |
| **Formato** | PyArrow/Parquet | Compressão e performance |
| **Visualização** | Matplotlib/Seaborn | Gráficos profissionais |
| **ML** | Scikit-learn | Normalização e pré-processamento |

### 4.2 Tecnologias para Refinamento (Futuro)

| Tecnologia | Justificativa | Benefício |
|------------|---------------|-----------|
| **Apache Spark** | Processamento distribuído | Escalabilidade para datasets maiores |
| **Apache Airflow** | Orquestração de pipelines | Automação e monitoramento |
| **Apache Kafka** | Streaming de dados | Processamento em tempo real |
| **MLflow** | Gestão de modelos ML | Versionamento e deploy de modelos |
| **Tableau/Power BI** | Dashboards interativos | Visualizações dinâmicas |
| **Apache Superset** | BI self-service | Análises ad-hoc pelos usuários |

---

## 5. Arquitetura Parcial Implementada

### 5.1 Ambiente Atual
- **Ambiente:** Jupyter Notebooks
- **Armazenamento:** Sistema de arquivos local
- **Processamento:** Single-node (local)

### 5.2 Simulação de Big Data
- **Arquitetura Medallion:** Implementada completamente
- **Pipeline ETL:** Processo completo documentado
- **Qualidade de dados:** Validações implementadas
- **Metadados:** Rastreabilidade completa

### 5.3 Escalabilidade
O pipeline atual pode ser facilmente escalado para:
- **Cloud Computing:** AWS/Azure/GCP
- **Processamento distribuído:** Apache Spark
- **Streaming:** Apache Kafka
- **Orquestração:** Apache Airflow

---

## 6. Divisão de Responsabilidades

### 6.1 Leonardo Azevedo
- **Responsabilidade:** Ingestão e Arquitetura de Dados
- **Entregáveis:**
  - Notebook 01 (Ingestão)
  - Estrutura de pastas Medallion
  - Validações de qualidade
  - Documentação técnica

### 6.2 Walter Barreto
- **Responsabilidade:** Transformação e Engenharia de Features
- **Entregáveis:**
  - Notebook 02 (Transformação)
  - Criação de 10 novas features
  - Normalização e agregações
  - Otimização de performance

### 6.3 Mariana Belo
- **Responsabilidade:** Análise e Visualização
- **Entregáveis:**
  - Notebook 03 (Análise)
  - 7 visualizações profissionais
  - Dashboard executivo
  - Insights estratégicos

---

## 7. Próximos Passos

### 7.1 Melhorias Técnicas
1. Implementar modelo de Machine Learning
2. Criar sistema de alertas automáticos
3. Desenvolver API para consultas
4. Implementar monitoramento contínuo

### 7.2 Expansão do Pipeline
1. Integração com fontes de dados em tempo real
2. Implementação de streaming processing
3. Criação de dashboards interativos
4. Deploy em ambiente cloud

---

## 8. Conclusão

O pipeline implementado demonstra uma solução completa de Big Data para análise de churn, seguindo as melhores práticas da indústria. A arquitetura Medallion garante qualidade e rastreabilidade dos dados, enquanto as tecnologias escolhidas proporcionam eficiência e escalabilidade.

**Status atual:** ✅ Pipeline completo implementado e funcional  
**Próxima entrega:** Modelo preditivo e sistema de alertas  
**Data:** 13/10/2024
