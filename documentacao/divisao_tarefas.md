# Divisão de Tarefas - Pipeline de Big Data
## Análise de Churn Telecom

**Equipe:** Leonardo Azevedo, Walter Barreto, Mariana Belo  
**Data:** 13/10/2024  
**Disciplina:** Fundamentos de Big Data  

---

## 👥 Visão Geral da Equipe

### **Objetivo da Divisão**
Distribuir as responsabilidades de forma equilibrada, garantindo que cada membro tenha experiência prática em diferentes etapas do pipeline de Big Data, promovendo aprendizado colaborativo e desenvolvimento de habilidades complementares.

---

## 🎯 Leonardo Azevedo
### **Responsabilidade Principal:** Ingestão e Arquitetura de Dados

#### **📥 Tarefas de Ingestão**
- [x] **Configuração do ambiente**
  - Criação da estrutura de pastas Medallion
  - Configuração de imports e bibliotecas
  - Setup inicial do ambiente de desenvolvimento

- [x] **Implementação da ingestão**
  - Desenvolvimento de função inteligente para obter dataset
  - Download automático do GitHub com fallback
  - Validação de integridade dos dados
  - Tratamento de erros e exceções

- [x] **Qualidade e metadados**
  - Adição de metadados de ingestão (data, fonte)
  - Validação de duplicatas
  - Verificação de consistência dos dados
  - Geração de relatório de ingestão

#### **🏗️ Tarefas de Arquitetura**
- [x] **Design da arquitetura**
  - Definição da arquitetura Medallion
  - Criação de diagramas de fluxo
  - Documentação técnica da arquitetura

- [x] **Estrutura de dados**
  - Organização das camadas Bronze/Silver/Gold
  - Definição de padrões de nomenclatura
  - Estruturação do repositório

#### **📊 Entregáveis**
- Notebook `01_ingestao.ipynb` completo
- Documento de arquitetura detalhado
- Estrutura de pastas organizada
- Relatório de ingestão
- Validações de qualidade implementadas

---

## 🔧 Walter Barreto
### **Responsabilidade Principal:** Transformação e Engenharia de Features

#### **🧹 Tarefas de Limpeza**
- [x] **Tratamento de dados ausentes**
  - Conversão de TotalCharges para numérico
  - Tratamento de 11 valores ausentes
  - Estratégias de preenchimento inteligente

- [x] **Validação de qualidade**
  - Remoção de duplicatas
  - Verificação de consistência
  - Validação de tipos de dados

#### **⚙️ Tarefas de Engenharia de Features**
- [x] **Criação de features derivadas**
  - `AvgChargePerMonth`: Valor médio por mês
  - `TenureGroup`: Categorização de tempo
  - `IsPremium`: Flag de cliente premium
  - `NumServicos`: Contagem de serviços
  - `HasSecurity`: Flag de segurança
  - `SatisfactionScore`: Score de satisfação
  - `ChurnRiskScore`: Score de risco
  - Normalizações (MinMaxScaler)

#### **📈 Tarefas de Agregação**
- [x] **Criação de datasets Gold**
  - Métricas por tipo de contrato
  - Análise de churn por segmento
  - Perfil de clientes de alto risco
  - Correlações com churn

#### **📊 Entregáveis**
- Notebook `02_transformacao.ipynb` completo
- 10 novas features criadas
- 4 datasets Gold gerados
- Otimização de performance (Parquet)
- Relatório de transformação

---

## 📊 Mariana Belo
### **Responsabilidade Principal:** Análise e Visualização

#### **🔍 Tarefas de Análise Exploratória**
- [x] **Análise estatística**
  - Distribuição de churn (26.54%)
  - Análise por tipo de contrato
  - Análise por tempo de permanência
  - Impacto dos serviços contratados

- [x] **Descoberta de insights**
  - Identificação de perfis de risco
  - Análise de impacto financeiro
  - Correlações entre variáveis
  - Padrões comportamentais

#### **📈 Tarefas de Visualização**
- [x] **Criação de gráficos profissionais**
  - Distribuição de churn (barras + pizza)
  - Churn por tipo de contrato
  - Análise de tenure (histograma + barras)
  - Charges vs churn (boxplots)
  - Impacto dos serviços (linha + barras)
  - Matriz de correlação (heatmap)
  - Score de satisfação vs churn

- [x] **Dashboard executivo**
  - Métricas principais consolidadas
  - Visualizações integradas
  - Layout profissional
  - Exportação em alta qualidade

#### **💡 Tarefas de Insights Estratégicos**
- [x] **Recomendações de negócio**
  - Priorização de contratos longos
  - Promoção de múltiplos serviços
  - Foco em serviços de segurança
  - Intervenção nos primeiros 12 meses
  - Segmentação de clientes premium

#### **📊 Entregáveis**
- Notebook `03_analise_visualizacao.ipynb` completo
- 7 visualizações profissionais (PNG)
- Dashboard executivo consolidado
- Relatório final com insights
- Recomendações estratégicas

---

## 🤝 Colaboração e Integração

### **🔄 Fluxo de Trabalho**
1. **Leonardo** → Ingestão e estruturação inicial
2. **Walter** → Transformação e enriquecimento dos dados
3. **Mariana** → Análise e geração de insights
4. **Todos** → Revisão, documentação e apresentação

### **📋 Responsabilidades Compartilhadas**
- [x] **Documentação**
  - README.md atualizado
  - Comentários no código
  - Relatórios técnicos

- [x] **Qualidade**
  - Revisão cruzada dos notebooks
  - Validação de resultados
  - Testes de integridade

- [x] **Apresentação**
  - Preparação para demonstração
  - Slides de apresentação
  - Defesa técnica

---

## 📊 Métricas de Contribuição

### **Leonardo Azevedo**
- **Linhas de código:** ~200 linhas
- **Commits:** 5 commits principais
- **Arquivos criados:** 2 (notebook + documentação)
- **Foco:** Ingestão e arquitetura

### **Walter Barreto**
- **Linhas de código:** ~300 linhas
- **Commits:** 6 commits principais
- **Arquivos criados:** 2 (notebook + datasets)
- **Foco:** Transformação e features

### **Mariana Belo**
- **Linhas de código:** ~300 linhas
- **Commits:** 4 commits principais
- **Arquivos criados:** 2 (notebook + visualizações)
- **Foco:** Análise e visualização

---

## 🎯 Equilíbrio da Divisão

### **✅ Pontos Fortes da Divisão**

1. **Especialização por Etapa**
   - Cada membro domina uma fase específica
   - Expertise técnica aprofundada
   - Responsabilidades claras

2. **Complementaridade**
   - Habilidades técnicas diversificadas
   - Perspectivas diferentes do problema
   - Aprendizado colaborativo

3. **Balanceamento de Carga**
   - Tarefas distribuídas equilibradamente
   - Tempo de desenvolvimento similar
   - Entregáveis proporcionais

### **🔄 Rotação de Responsabilidades**
Para futuros projetos, a equipe pode rotacionar as responsabilidades para que todos tenham experiência completa no pipeline de Big Data.

---

## 🚀 Próximos Passos (AV2)

### **Responsabilidades Futuras**
- **Leonardo:** Infraestrutura e deploy
- **Walter:** Modelos de Machine Learning
- **Mariana:** Dashboards interativos e APIs

### **Colaboração Contínua**
- Reuniões semanais de alinhamento
- Code reviews entre membros
- Documentação colaborativa
- Apresentações conjuntas

---

## ✅ Status Final

**Divisão de Tarefas:** ✅ **BALANCEADA E EFETIVA**

- ✅ Responsabilidades claras definidas
- ✅ Carga de trabalho equilibrada
- ✅ Entregáveis distribuídos proporcionalmente
- ✅ Colaboração efetiva implementada
- ✅ Aprendizado mútuo promovido

**Equipe pronta para apresentação e próximas etapas!**

---

**Data de Conclusão:** 13/10/2024  
**Versão:** 1.0 (AV1)  
**Status:** ✅ DIVISÃO APROVADA E IMPLEMENTADA
