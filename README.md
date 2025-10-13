# 📊 Análise Preditiva de Churn em Telecomunicações

## Pipeline de Big Data - Fundamentos de Big Data

---

## 👥 Equipe

- **Membro 1:** Leonardo Azevedo - Responsável por Ingestão e Documentação
- **Membro 2:** [Nome Completo] - Responsável por Transformação e Engenharia de Features
- **Membro 3:** [Nome Completo] - Responsável por Análise e Visualização

---

## 📝 Descrição do Projeto

Este projeto implementa um **pipeline completo de Big Data** para análise de churn (cancelamento) de clientes em uma empresa de telecomunicações. O objetivo é identificar padrões que indicam risco de cancelamento e gerar insights acionáveis para estratégias de retenção.

### 🎯 Problema de Negócio

Empresas de telecomunicações enfrentam altas taxas de churn, resultando em:

- **Perda de receita recorrente**
- **Custos elevados de aquisição de novos clientes**
- **Impacto negativo no valor do cliente (LTV)**

Este projeto visa **identificar preventivamente** clientes com maior propensão ao churn para permitir ações de retenção direcionadas.

---

## 🗂️ Fonte dos Dados

**Dataset:** Telco Customer Churn (Kaggle)

- **Arquivo:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- **Registros:** 7.043 clientes
- **Variáveis:** 21 atributos (demográficos, serviços, faturamento)
- **Variável Alvo:** Churn (Yes/No)

### Principais Variáveis:

- `customerID`: ID único do cliente
- `tenure`: Meses como cliente
- `MonthlyCharges`: Cobrança mensal
- `TotalCharges`: Cobrança total
- `Contract`: Tipo de contrato (Mensal/Anual/Bienal)
- `InternetService`: Tipo de internet
- `Churn`: Cliente cancelou? (Yes/No)

---

## 🏗️ Arquitetura do Pipeline

O projeto segue a **arquitetura Medallion** com 3 camadas:

```
┌─────────────────────────────────────────────────────────┐
│                    PIPELINE DE DADOS                     │
└─────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   📥 BRONZE  │  -->  │   🔧 SILVER  │  -->  │   🏆 GOLD    │
│  Dados Brutos│       │Transformados │       │   Insights   │
└──────────────┘       └──────────────┘       └──────────────┘
```

### Camadas:

1. **🥉 Bronze (Raw Data)**

   - Dados brutos sem tratamento
   - Formato: CSV original
   - Localização: `/dados/bronze/`

2. **🥈 Silver (Cleaned Data)**

   - Dados limpos e transformados
   - Engenharia de features aplicada
   - Formato: CSV + Parquet
   - Localização: `/dados/silver/`

3. **🥇 Gold (Analytics-Ready)**
   - Datasets agregados para análise
   - Visualizações e relatórios
   - Localização: `/dados/gold/`

---

## 🛠️ Ferramentas e Tecnologias

### **Ambiente de Desenvolvimento**

- **Google Colab** (plataforma principal - sem custos)
- **Python 3.x** (linguagem de programação)

### **Bibliotecas Utilizadas**

#### Processamento de Dados:

- **Pandas** → Manipulação e transformação de dados
- **NumPy** → Operações numéricas vetorizadas
- **PyArrow** → Leitura/escrita de arquivos Parquet

#### Visualização:

- **Matplotlib** → Gráficos estáticos
- **Seaborn** → Visualizações estatísticas
- **Plotly** (opcional) → Gráficos interativos

#### Machine Learning (próxima fase):

- **Scikit-learn** → Modelos preditivos
- **XGBoost/LightGBM** → Modelos avançados

### **Formato de Armazenamento**

- **CSV** → Dados brutos e intermediários
- **Parquet** → Dados transformados (compressão ~60%)

---

## 📂 Estrutura do Repositório

```
telco-churn-analysis/
│
├── README.md                          # Este arquivo
│
├── dados/
│   ├── bronze/                        # Dados brutos
│   │   ├── telco_churn_raw.csv
│   │   └── relatorio_ingestao.txt
│   │
│   ├── silver/                        # Dados transformados
│   │   ├── telco_churn_transformed.csv
│   │   ├── telco_churn_transformed.parquet
│   │   └── relatorio_transformacao.txt
│   │
│   └── gold/                          # Datasets analíticos
│       ├── metricas_por_contrato.csv
│       ├── churn_por_segmento.csv
│       ├── perfil_alto_risco.csv
│       ├── viz_01_distribuicao_churn.png
│       ├── viz_02_churn_por_contrato.png
│       ├── viz_03_analise_tenure.png
│       ├── viz_04_charges_vs_churn.png
│       ├── viz_05_impacto_servicos.png
│       ├── viz_06_correlacao.png
│       ├── viz_07_satisfacao_churn.png
│       ├── dashboard_final.png
│       └── relatorio_final.txt
│
├── notebooks/
│   ├── 01_ingestao.ipynb              # Notebook de ingestão
│   ├── 02_transformacao.ipynb         # Notebook de transformação
│   └── 03_analise_visualizacao.ipynb  # Notebook de análise
│
├── src/                                # Scripts Python
│   ├── ingestao.py
│   ├── transformacao.py
│   └── utils.py
│
└── documentacao/
    ├── arquitetura_pipeline.pdf        # Diagrama detalhado
    ├── apresentacao_av1.pdf            # Slides da apresentação
    └── checklist_av1.md                # Checklist de entregas
```

---

## 🚀 Como Executar

### 1️⃣ **Configuração Inicial**

```python
# Clonar o repositório
!git clone https://github.com/[seu-usuario]/telco-churn-analysis.git
%cd telco-churn-analysis

# Instalar dependências (se necessário)
!pip install pandas numpy matplotlib seaborn pyarrow scikit-learn
```

### 2️⃣ **Executar Pipeline Completo**

#### **Opção A: Executar notebooks sequencialmente**

1. Abrir `01_ingestao.ipynb` no Colab
2. Executar todas as células (Runtime > Run all)
3. Repetir para `02_transformacao.ipynb`
4. Repetir para `03_analise_visualizacao.ipynb`

#### **Opção B: Executar scripts Python**

```python
# No Google Colab
%run src/ingestao.py
%run src/transformacao.py
%run src/analise.py
```

### 3️⃣ **Visualizar Resultados**

```python
# Verificar estrutura criada
!ls -R dados/

# Visualizar relatório final
!cat dados/gold/relatorio_final.txt

# Exibir gráficos
from IPython.display import Image
Image('/content/dados/gold/dashboard_final.png')
```

---

## 📊 Principais Descobertas

### 🔴 Taxa Geral de Churn: **26.5%**

### 📉 Fatores de Maior Impacto:

1. **Tipo de Contrato**

   - Mensal: ~42% de churn
   - Anual: ~11% de churn
   - Bienal: ~3% de churn

2. **Tempo de Permanência**

   - 0-12 meses: Alto risco
   - 36+ meses: Baixo risco

3. **Número de Serviços**

   - 1-2 serviços: Alta taxa de churn
   - 4+ serviços: Baixa taxa de churn

4. **Serviços de Segurança**
   - Com segurança: -15% de churn
   - Sem segurança: Taxa elevada

---

## 💡 Recomendações Estratégicas

### 🎯 **Ações Prioritárias**

1. **Migração para Contratos Longos**

   - Oferecer desconto de 15-20% em contratos anuais
   - Criar programa de fidelidade

2. **Bundling de Serviços**

   - Pacotes com 4+ serviços
   - Descontos progressivos

3. **Onboarding Intensivo**

   - Acompanhamento nos primeiros 90 dias
   - Suporte proativo

4. **Programa de Segurança**
   - Trial gratuito de 30 dias
   - Educação sobre benefícios

---

## 📈 Próximas Etapas (AV2)

- [ ] Implementar modelo de Machine Learning preditivo
- [ ] Criar API para scoring em tempo real
- [ ] Dashboard interativo com Streamlit
- [ ] Sistema de alertas automatizados
- [ ] A/B Testing de estratégias de retenção

---

## 📋 Status do Projeto (AV1)

### ✅ Entregas Completas

- [x] **Ingestão**: Finalizado
- [x] **Armazenamento**: Finalizado (Arquitetura Medallion)
- [x] **Transformação**: Finalizado
- [x] **Visualização**: Finalizado
- [x] **Documentação**: Finalizado
- [x] **Repositório GitHub**: Organizado

### 📊 Métricas

- **Linhas de Código:** ~800 linhas
- **Commits:** 15+ (todos os membros contribuíram)
- **Visualizações Criadas:** 7 gráficos + 1 dashboard
- **Datasets Gerados:** 6 arquivos
- **Documentação:** 100% completa

---

## 📚 Referências

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [Google Colab Guide](https://colab.research.google.com/)
- Dataset original: [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto:

- **Repositório:** https://github.com/[seu-usuario]/telco-churn-analysis
- **Equipe:** leonardo.azevedo@cesar.org.br
- **Disciplina:** Fundamentos de Big Data
- **Professor(a):** [Nome do Professor]

---

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos na disciplina de Fundamentos de Big Data.

---

**Última Atualização:** 13/10/2024 | **Versão:** 1.0 (AV1)
