# Checklist AV1 - Pipeline de Big Data
## Análise de Churn Telecom

**Equipe:** Leonardo Azevedo, Walter Barreto, Mariana Belo  
**Data:** 13/10/2024  
**Disciplina:** Fundamentos de Big Data  

---

## 📋 Checklist de Entregas AV1

### ✅ 1. Documento de Arquitetura (PDF ou DOCX)

- [x] **Diagrama do pipeline de dados atual**
  - Arquitetura Medallion implementada (Bronze-Silver-Gold)
  - Fluxo de dados documentado
  - Diagramas ASCII criados

- [x] **Tecnologias utilizadas e justificativa**
  - Python, Pandas, NumPy, Matplotlib, Seaborn
  - PyArrow para formato Parquet
  - Scikit-learn para normalização
  - Tecnologias futuras identificadas (Spark, Airflow, Kafka)

- [x] **Arquitetura parcial implementada**
  - Pipeline completo funcional
  - Ambiente Jupyter Notebooks
  - Estrutura de pastas organizada
  - Simulação de Big Data com arquitetura escalável

- [x] **Equipe responsável e divisão de tarefas**
  - Leonardo Azevedo: Ingestão e Arquitetura
  - Walter Barreto: Transformação e Features
  - Mariana Belo: Análise e Visualização

---

### ✅ 2. Repositório GitHub do Grupo

- [x] **Estrutura organizada**
  - `/dados` (amostras de dados) ✅
  - `/src` (scripts e notebooks) ✅
  - `/documentacao` (diagramas, PDFs, etc.) ✅

- [x] **README inicial completo**
  - Nome e descrição do projeto ✅
  - Fonte dos dados (Kaggle Telco Churn) ✅
  - Ferramentas aplicadas (Python, Pandas, etc.) ✅
  - Instruções de execução ✅
  - Principais descobertas ✅

- [x] **Commits visíveis e mensagens claras**
  - Histórico de commits organizado ✅
  - Contribuições de todos os membros ✅
  - Mensagens descritivas ✅

---

### ✅ 3. Demonstração Técnica (em aula)

- [x] **Funcionamento da ingestão**
  - Download automático do dataset ✅
  - Validação de integridade ✅
  - Salvamento na camada Bronze ✅
  - 7.043 registros processados ✅

- [x] **Funcionamento da transformação**
  - Limpeza de dados (11 valores ausentes tratados) ✅
  - 10 novas features criadas ✅
  - Normalização aplicada ✅
  - Salvamento em CSV e Parquet ✅

- [x] **Funcionamento da análise**
  - 7 visualizações profissionais ✅
  - Dashboard executivo ✅
  - Insights estratégicos ✅
  - Relatório final completo ✅

---

### ✅ 4. Checklist Preenchido

#### **Ingestão:** ✅ Finalizado
- [x] Download automático do dataset
- [x] Validação de integridade dos dados
- [x] Criação da estrutura Bronze
- [x] Adição de metadados de ingestão
- [x] Relatório de ingestão gerado

#### **Armazenamento:** ✅ Finalizado
- [x] Arquitetura Medallion implementada
- [x] Camada Bronze (dados brutos)
- [x] Camada Silver (dados transformados)
- [x] Camada Gold (insights e visualizações)
- [x] Formato Parquet para otimização

#### **Transformação:** ✅ Finalizado
- [x] Limpeza de dados completa
- [x] Engenharia de features (10 novas)
- [x] Normalização de variáveis
- [x] Agregações estatísticas
- [x] Validação de qualidade
- [x] Otimização de performance

---

## 📊 Métricas de Qualidade

### **Dados Processados**
- **Registros:** 7.043 clientes
- **Features originais:** 23 colunas
- **Features após transformação:** 33 colunas
- **Novas features criadas:** 10
- **Valores ausentes:** 0 (após tratamento)
- **Duplicatas:** 0

### **Performance**
- **Redução de tamanho:** 80.7% (Parquet vs CSV)
- **Tempo de processamento:** < 2 minutos
- **Memória utilizada:** Otimizada
- **Qualidade dos dados:** 100% validada

### **Entregáveis**
- **Notebooks:** 3 notebooks completos
- **Visualizações:** 7 gráficos + 1 dashboard
- **Datasets:** 6 arquivos Gold
- **Documentação:** 100% completa
- **Código:** ~800 linhas

---

## 🎯 Principais Descobertas

### **Taxa de Churn:** 26.54%

### **Fatores Críticos:**
1. **Tipo de Contrato**
   - Mensal: 42.7% de churn
   - Anual: 11.3% de churn
   - Bienal: 2.8% de churn

2. **Tempo de Permanência**
   - Novos (0-12 meses): 47.4% de churn
   - Médio (13-36 meses): 25.5% de churn
   - Longo (36+ meses): 11.9% de churn

3. **Impacto Financeiro**
   - Receita mensal perdida: R$ 139.130,85
   - Receita total perdida: R$ 2.862.926,90
   - Ticket médio dos churns: R$ 74,44

---

## 🚀 Próximos Passos (AV2)

- [ ] Implementar modelo de Machine Learning
- [ ] Criar sistema de alertas automáticos
- [ ] Desenvolver API para consultas
- [ ] Dashboard interativo
- [ ] Monitoramento contínuo

---

## ✅ Status Final

**Pipeline Status:** ✅ **COMPLETO E FUNCIONAL**

- ✅ Ingestão: Finalizado
- ✅ Armazenamento: Finalizado
- ✅ Transformação: Finalizado
- ✅ Análise: Finalizado
- ✅ Visualização: Finalizado
- ✅ Documentação: Finalizada

**Pronto para apresentação em aula!**

---

**Data de Conclusão:** 13/10/2024  
**Versão:** 1.0 (AV1)  
**Status:** ✅ APROVADO PARA APRESENTAÇÃO
