"""
ingestao.py
Script para ingestão de dados - Camada Bronze
Pipeline de Big Data - Análise de Churn Telecom
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Dict
import sys
import os

# Importar funções utilitárias
try:
    from utils import (
        criar_estrutura_pastas,
        adicionar_metadados,
        validar_dados_brutos,
        gerar_relatorio_texto,
        calcular_estatisticas_churn,
        imprimir_separador,
        validar_colunas_obrigatorias,
        salvar_dataframe_multiplos_formatos,
        log_progresso,
        COLUNAS_OBRIGATORIAS,
    )
except ImportError:
    print("⚠️ Não foi possível importar utils.py")
    print("   Certifique-se que utils.py está na mesma pasta ou no PYTHONPATH")


class IngestorDados:
    """
    Classe responsável pela ingestão de dados brutos na Camada Bronze

    Responsabilidades:
    - Ler dados de arquivos CSV
    - Validar estrutura e qualidade
    - Adicionar metadados de rastreabilidade
    - Salvar dados brutos na camada Bronze
    - Gerar relatórios de ingestão
    """

    def __init__(self, caminho_base: str = "/content/dados"):
        """
        Inicializa o ingestor de dados

        Args:
            caminho_base: Diretório base para armazenar dados (padrão: /content/dados)
        """
        self.caminho_base = caminho_base
        self.caminho_bronze = f"{caminho_base}/bronze"
        self.caminho_silver = f"{caminho_base}/silver"
        self.caminho_gold = f"{caminho_base}/gold"
        self.timestamp_inicio = datetime.now()

        print(f"🔧 IngestorDados inicializado")
        print(f"   Base: {self.caminho_base}")
        print(f"   Bronze: {self.caminho_bronze}")

    def configurar_ambiente(self) -> None:
        """
        Configura o ambiente criando estrutura de pastas necessária
        Cria as camadas: Bronze, Silver e Gold
        """
        log_progresso("Configurando ambiente...", "INFO")
        criar_estrutura_pastas(self.caminho_base)
        log_progresso("Ambiente configurado com sucesso", "SUCCESS")

    def ingerir_csv(
        self,
        caminho_arquivo: str,
        nome_fonte: str = "Kaggle_TelcoChurn",
        encoding: str = "utf-8",
        separator: str = ",",
    ) -> pd.DataFrame:
        """
        Ingere dados de arquivo CSV

        Args:
            caminho_arquivo: Caminho do arquivo CSV a ser lido
            nome_fonte: Nome identificador da fonte dos dados
            encoding: Encoding do arquivo (padrão: utf-8)
            separator: Separador do CSV (padrão: vírgula)

        Returns:
            DataFrame com dados ingeridos e metadados adicionados

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            Exception: Para outros erros na leitura
        """
        imprimir_separador("INGESTÃO DE DADOS", caractere="=")

        try:
            log_progresso(f"Lendo arquivo: {caminho_arquivo}", "INFO")

            # Ler CSV
            df = pd.read_csv(caminho_arquivo, encoding=encoding, sep=separator)

            log_progresso(f"Arquivo lido com sucesso!", "SUCCESS")
            log_progresso(f"Registros: {len(df):,}", "INFO")
            log_progresso(f"Colunas: {len(df.columns)}", "INFO")

            # Adicionar metadados de rastreabilidade
            df = adicionar_metadados(df, nome_fonte)
            log_progresso("Metadados de rastreabilidade adicionados", "SUCCESS")

            # Mostrar preview
            print("\n📋 Preview dos dados (primeiras 3 linhas):")
            print(df.head(3))

            return df

        except FileNotFoundError:
            log_progresso(f"Arquivo não encontrado: {caminho_arquivo}", "ERROR")
            log_progresso("Verifique se o caminho está correto", "ERROR")
            raise

        except pd.errors.EmptyDataError:
            log_progresso("Arquivo CSV está vazio", "ERROR")
            raise

        except Exception as e:
            log_progresso(f"Erro na ingestão: {str(e)}", "ERROR")
            raise

    def validar_estrutura(self, df: pd.DataFrame) -> Dict:
        """
        Valida a estrutura dos dados ingeridos

        Verifica:
        - Presença de colunas obrigatórias
        - Tipos de dados
        - Valores ausentes
        - Duplicatas
        - Uso de memória

        Args:
            df: DataFrame a ser validado

        Returns:
            Dicionário com resultados da validação e métricas de qualidade
        """
        imprimir_separador("VALIDAÇÃO DE ESTRUTURA")

        # 1. Verificar colunas obrigatórias
        log_progresso("Verificando colunas obrigatórias...", "INFO")
        todas_presentes, faltantes = validar_colunas_obrigatorias(
            df, COLUNAS_OBRIGATORIAS
        )

        if not todas_presentes:
            log_progresso(f"⚠️ Colunas faltantes: {faltantes}", "WARNING")
        else:
            log_progresso("Todas as colunas obrigatórias presentes", "SUCCESS")

        # 2. Validar qualidade geral
        log_progresso("Validando qualidade dos dados...", "INFO")
        validacao = validar_dados_brutos(df)

        # 3. Mostrar métricas
        print("\n📊 Métricas de Qualidade:")
        print(f"   • Registros: {validacao['total_registros']:,}")
        print(f"   • Colunas: {validacao['total_colunas']}")
        print(f"   • Duplicatas: {validacao['duplicatas']}")
        print(f"   • Valores ausentes: {validacao['valores_ausentes']}")
        print(f"   • Memória: {validacao['memoria_mb']:.2f} MB")

        # 4. Mostrar colunas com valores ausentes
        if validacao["colunas_com_ausentes"]:
            print("\n⚠️ Colunas com valores ausentes:")
            for col, count in validacao["colunas_com_ausentes"].items():
                print(f"   • {col}: {count} valores")

        # 5. Verificar tipos de dados
        print("\n📋 Tipos de dados:")
        tipos_unicos = df.dtypes.value_counts()
        for tipo, count in tipos_unicos.items():
            print(f"   • {tipo}: {count} colunas")

        log_progresso("Validação de estrutura concluída", "SUCCESS")

        return validacao

    def explorar_dados(self, df: pd.DataFrame) -> Dict:
        """
        Realiza exploração inicial dos dados ingeridos

        Análises:
        - Estatísticas descritivas
        - Distribuição de churn
        - Valores únicos em colunas categóricas

        Args:
            df: DataFrame a ser explorado

        Returns:
            Dicionário com estatísticas exploratórias
        """
        imprimir_separador("EXPLORAÇÃO INICIAL DOS DADOS")

        # 1. Dimensões
        print("\n📐 Dimensões do dataset:")
        print(f"   • Linhas: {df.shape[0]:,}")
        print(f"   • Colunas: {df.shape[1]}")

        # 2. Preview dos dados
        print("\n📋 Primeiras 5 linhas:")
        print(df.head())

        # 3. Informações de tipos
        print("\n📊 Informações dos tipos de dados:")
        df.info()

        # 4. Estatísticas descritivas para variáveis numéricas
        print("\n🔢 Estatísticas descritivas (variáveis numéricas):")
        print(df.describe())

        # 5. Estatísticas de churn
        try:
            stats_churn = calcular_estatisticas_churn(df)

            print("\n📈 Estatísticas de Churn:")
            print(f"   • Total de clientes: {stats_churn['total_clientes']:,}")
            print(f"   • Clientes ativos: {stats_churn['clientes_ativos']:,}")
            print(f"   • Clientes com churn: {stats_churn['clientes_churn']:,}")
            print(f"   • Taxa de churn: {stats_churn['taxa_churn_percentual']:.2f}%")

            # Visualizar distribuição
            print("\n📊 Distribuição da variável Churn:")
            print(df["Churn"].value_counts())

        except Exception as e:
            log_progresso(f"Erro ao calcular estatísticas de churn: {e}", "WARNING")
            stats_churn = {}

        # 6. Valores únicos em colunas categóricas selecionadas
        print("\n🏷️ Valores únicos em colunas categóricas principais:")
        colunas_cat = ["gender", "Contract", "InternetService", "PaymentMethod"]
        for col in colunas_cat:
            if col in df.columns:
                print(f"\n   {col}:")
                print(f"   {df[col].value_counts()}")

        log_progresso("Exploração inicial concluída", "SUCCESS")

        return stats_churn

    def salvar_bronze(
        self, df: pd.DataFrame, nome_arquivo: str = "telco_churn_raw.csv"
    ) -> str:
        """
        Salva dados na camada Bronze (dados brutos sem transformação)

        Args:
            df: DataFrame a ser salvo
            nome_arquivo: Nome do arquivo de saída

        Returns:
            Caminho completo do arquivo salvo

        Raises:
            Exception: Se houver erro ao salvar
        """
        imprimir_separador("SALVANDO NA CAMADA BRONZE")

        caminho_output = f"{self.caminho_bronze}/{nome_arquivo}"

        try:
            # Salvar CSV
            df.to_csv(caminho_output, index=False)
            log_progresso(f"Arquivo salvo: {caminho_output}", "SUCCESS")

            # Calcular e mostrar tamanho
            tamanho_mb = os.path.getsize(caminho_output) / 1024 / 1024
            log_progresso(f"Tamanho do arquivo: {tamanho_mb:.2f} MB", "INFO")

            # Verificar integridade
            df_verificacao = pd.read_csv(caminho_output)
            if len(df_verificacao) == len(df):
                log_progresso(
                    f"Integridade verificada: {len(df):,} registros", "SUCCESS"
                )
            else:
                log_progresso("Erro de integridade detectado!", "ERROR")

            return caminho_output

        except PermissionError:
            log_progresso(f"Sem permissão para escrever em: {caminho_output}", "ERROR")
            raise

        except Exception as e:
            log_progresso(f"Erro ao salvar arquivo: {str(e)}", "ERROR")
            raise

    def gerar_relatorio(self, metricas: Dict) -> None:
        """
        Gera relatório detalhado de ingestão

        Args:
            metricas: Dicionário com métricas da ingestão
        """
        imprimir_separador("GERANDO RELATÓRIO")

        caminho_relatorio = f"{self.caminho_bronze}/relatorio_ingestao.txt"

        tempo_execucao = (datetime.now() - self.timestamp_inicio).total_seconds()

        metricas_relatorio = {
            "Data e Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Registros Ingeridos": f"{metricas.get('total_registros', 0):,}",
            "Colunas": metricas.get("total_colunas", 0),
            "Duplicatas Encontradas": metricas.get("duplicatas", 0),
            "Valores Ausentes": metricas.get("valores_ausentes", 0),
            "Uso de Memória": f"{metricas.get('memoria_mb', 0):.2f} MB",
            "Taxa de Churn": f"{metricas.get('taxa_churn_percentual', 0):.2f}%",
            "Tempo de Execução": f"{tempo_execucao:.2f} segundos",
        }

        gerar_relatorio_texto(
            titulo="RELATÓRIO DE INGESTÃO DE DADOS",
            metricas=metricas_relatorio,
            caminho_output=caminho_relatorio,
        )

        log_progresso(f"Relatório salvo: {caminho_relatorio}", "SUCCESS")

    def executar_pipeline_completo(self, caminho_arquivo: str) -> pd.DataFrame:
        """
        Executa o pipeline completo de ingestão de dados

        Pipeline:
        1. Configura ambiente (cria pastas)
        2. Ingere dados do CSV
        3. Valida estrutura
        4. Explora dados
        5. Salva na camada Bronze
        6. Gera relatório

        Args:
            caminho_arquivo: Caminho do arquivo CSV a ingerir

        Returns:
            DataFrame com dados ingeridos
        """
        imprimir_separador("🚀 PIPELINE DE INGESTÃO - INÍCIO", caractere="=")

        print(f"\n📂 Arquivo: {caminho_arquivo}")
        print(f"⏰ Início: {self.timestamp_inicio.strftime('%H:%M:%S')}")

        try:
            # Etapa 1: Configurar ambiente
            self.configurar_ambiente()

            # Etapa 2: Ingerir dados
            df = self.ingerir_csv(caminho_arquivo)

            # Etapa 3: Validar estrutura
            validacao = self.validar_estrutura(df)

            # Etapa 4: Explorar dados
            stats_churn = self.explorar_dados(df)

            # Etapa 5: Salvar na camada Bronze
            caminho_salvo = self.salvar_bronze(df)

            # Etapa 6: Gerar relatório
            metricas = {**validacao, **stats_churn}
            self.gerar_relatorio(metricas)

            # Finalização
            imprimir_separador("✅ PIPELINE DE INGESTÃO - CONCLUÍDO", caractere="=")

            tempo_total = (datetime.now() - self.timestamp_inicio).total_seconds()

            print(f"\n📊 Resumo da Execução:")
            print(f"   • Registros processados: {len(df):,}")
            print(f"   • Arquivo salvo: {caminho_salvo}")
            print(f"   • Tempo total: {tempo_total:.2f}s")
            print(f"   • Status: ✅ SUCESSO")

            return df

        except Exception as e:
            imprimir_separador("❌ PIPELINE DE INGESTÃO - ERRO", caractere="=")
            log_progresso(f"Erro no pipeline: {str(e)}", "ERROR")
            raise


def main():
    """
    Função principal para execução standalone do script
    Permite executar via linha de comando
    """
    import argparse

    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description="Script de Ingestão de Dados - Camada Bronze",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python ingestao.py --arquivo dados.csv
  python ingestao.py --arquivo dados.csv --base-path /meu/diretorio
        """,
    )

    parser.add_argument(
        "--arquivo",
        type=str,
        required=True,
        help="Caminho do arquivo CSV a ser ingerido",
    )

    parser.add_argument(
        "--base-path",
        type=str,
        default="/content/dados",
        help="Diretório base para salvar dados (padrão: /content/dados)",
    )

    parser.add_argument(
        "--fonte",
        type=str,
        default="Kaggle_TelcoChurn",
        help="Nome da fonte dos dados (padrão: Kaggle_TelcoChurn)",
    )

    args = parser.parse_args()

    # Executar pipeline
    print("=" * 60)
    print("INGESTÃO DE DADOS - PIPELINE DE BIG DATA")
    print("=" * 60)

    ingestor = IngestorDados(caminho_base=args.base_path)
    df = ingestor.executar_pipeline_completo(args.arquivo)

    print(f"\n✅ Pipeline executado com sucesso!")
    print(f"   Registros processados: {len(df):,}")
    print(f"   Próximo passo: Execute o script de transformação")


if __name__ == "__main__":
    main()


# ============================================================
# EXEMPLOS DE USO
# ============================================================

"""
EXEMPLO 1: Uso básico no Google Colab
--------------------------------------
from src.ingestao import IngestorDados

# Criar ingestor
ingestor = IngestorDados(caminho_base='/content/dados')

# Executar pipeline completo
df_bronze = ingestor.executar_pipeline_completo('WA_Fn-UseC_-Telco-Customer-Churn.csv')

print(f"Dados ingeridos: {len(df_bronze):,} registros")


EXEMPLO 2: Executar etapas separadamente
-----------------------------------------
from src.ingestao import IngestorDados

ingestor = IngestorDados()

# Etapa por etapa
ingestor.configurar_ambiente()
df = ingestor.ingerir_csv('arquivo.csv')
validacao = ingestor.validar_estrutura(df)
stats = ingestor.explorar_dados(df)
ingestor.salvar_bronze(df)
ingestor.gerar_relatorio({**validacao, **stats})


EXEMPLO 3: Via linha de comando
--------------------------------
# No terminal ou célula do Colab:
!python src/ingestao.py --arquivo dados.csv --base-path /content/dados


EXEMPLO 4: Personalizar fonte e encoding
-----------------------------------------
ingestor = IngestorDados()
df = ingestor.ingerir_csv(
    caminho_arquivo='dados.csv',
    nome_fonte='Minha_Fonte',
    encoding='latin-1'
)
"""
