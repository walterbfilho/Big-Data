"""
utils.py
Funções utilitárias compartilhadas para o pipeline de Big Data
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import json


def criar_estrutura_pastas(base_path: str = "/content/dados") -> None:
    """
    Cria a estrutura de pastas do projeto (Medallion Architecture)

    Args:
        base_path: Caminho base para criar as pastas
    """
    pastas = [f"{base_path}/bronze", f"{base_path}/silver", f"{base_path}/gold"]

    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)

    print("✅ Estrutura de pastas criada:")
    print(f"   - {base_path}/bronze  → Dados brutos")
    print(f"   - {base_path}/silver  → Dados transformados")
    print(f"   - {base_path}/gold    → Dados prontos para análise")


def adicionar_metadados(df: pd.DataFrame, fonte: str) -> pd.DataFrame:
    """
    Adiciona metadados de rastreabilidade ao DataFrame

    Args:
        df: DataFrame original
        fonte: Nome da fonte dos dados

    Returns:
        DataFrame com metadados adicionados
    """
    df_com_metadata = df.copy()
    df_com_metadata["data_ingestao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_com_metadata["fonte"] = fonte

    return df_com_metadata


def validar_dados_brutos(df: pd.DataFrame) -> Dict[str, any]:
    """
    Valida a qualidade dos dados brutos

    Args:
        df: DataFrame a ser validado

    Returns:
        Dicionário com métricas de qualidade
    """
    validacao = {
        "total_registros": len(df),
        "total_colunas": len(df.columns),
        "duplicatas": df.duplicated().sum(),
        "valores_ausentes": df.isnull().sum().sum(),
        "colunas_com_ausentes": df.isnull().sum()[df.isnull().sum() > 0].to_dict(),
        "tipos_dados": df.dtypes.to_dict(),
        "memoria_mb": df.memory_usage(deep=True).sum() / 1024**2,
    }

    return validacao


def gerar_relatorio_texto(titulo: str, metricas: Dict, caminho_output: str) -> None:
    """
    Gera relatório em formato texto

    Args:
        titulo: Título do relatório
        metricas: Dicionário com métricas para incluir
        caminho_output: Caminho onde salvar o relatório
    """
    relatorio = f"""
{'='*60}
{titulo}
{'='*60}
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

    for chave, valor in metricas.items():
        if isinstance(valor, dict):
            relatorio += f"\n{chave.upper()}:\n"
            for sub_chave, sub_valor in valor.items():
                relatorio += f"  - {sub_chave}: {sub_valor}\n"
        elif isinstance(valor, (int, float)):
            relatorio += f"{chave}: {valor:,}\n"
        else:
            relatorio += f"{chave}: {valor}\n"

    relatorio += f"\n{'='*60}\n"

    with open(caminho_output, "w", encoding="utf-8") as f:
        f.write(relatorio)

    print(f"📄 Relatório salvo em: {caminho_output}")


def comparar_tamanhos_arquivo(
    caminho_csv: str, caminho_parquet: str
) -> Dict[str, float]:
    """
    Compara tamanhos de arquivos CSV vs Parquet

    Args:
        caminho_csv: Caminho do arquivo CSV
        caminho_parquet: Caminho do arquivo Parquet

    Returns:
        Dicionário com tamanhos e redução percentual
    """
    tamanho_csv = os.path.getsize(caminho_csv) / 1024 / 1024  # MB
    tamanho_parquet = os.path.getsize(caminho_parquet) / 1024 / 1024  # MB
    reducao = ((tamanho_csv - tamanho_parquet) / tamanho_csv) * 100

    return {
        "csv_mb": round(tamanho_csv, 2),
        "parquet_mb": round(tamanho_parquet, 2),
        "reducao_percentual": round(reducao, 1),
    }


def calcular_estatisticas_churn(df: pd.DataFrame, coluna_churn: str = "Churn") -> Dict:
    """
    Calcula estatísticas básicas de churn

    Args:
        df: DataFrame com dados
        coluna_churn: Nome da coluna de churn

    Returns:
        Dicionário com estatísticas
    """
    if coluna_churn not in df.columns:
        raise ValueError(f"Coluna {coluna_churn} não encontrada no DataFrame")

    total = len(df)
    churns = (
        (df[coluna_churn] == "Yes").sum()
        if df[coluna_churn].dtype == "object"
        else df[coluna_churn].sum()
    )
    ativos = total - churns
    taxa = (churns / total) * 100

    return {
        "total_clientes": total,
        "clientes_ativos": ativos,
        "clientes_churn": churns,
        "taxa_churn_percentual": round(taxa, 2),
    }


def imprimir_separador(
    titulo: str = "", largura: int = 60, caractere: str = "="
) -> None:
    """
    Imprime um separador visual no console

    Args:
        titulo: Título opcional para incluir no separador
        largura: Largura do separador
        caractere: Caractere a usar no separador
    """
    if titulo:
        print(f"\n{caractere * largura}")
        print(f"{titulo.center(largura)}")
        print(f"{caractere * largura}")
    else:
        print(f"\n{caractere * largura}")


def validar_colunas_obrigatorias(
    df: pd.DataFrame, colunas_obrigatorias: List[str]
) -> Tuple[bool, List[str]]:
    """
    Valida se todas as colunas obrigatórias estão presentes

    Args:
        df: DataFrame a validar
        colunas_obrigatorias: Lista de colunas que devem estar presentes

    Returns:
        Tupla (todas_presentes: bool, colunas_faltantes: List[str])
    """
    colunas_presentes = set(df.columns)
    colunas_obrigatorias_set = set(colunas_obrigatorias)
    colunas_faltantes = list(colunas_obrigatorias_set - colunas_presentes)

    todas_presentes = len(colunas_faltantes) == 0

    return todas_presentes, colunas_faltantes


def salvar_dataframe_multiplos_formatos(
    df: pd.DataFrame,
    base_path: str,
    base_filename: str,
    formatos: List[str] = ["csv", "parquet"],
) -> Dict[str, str]:
    """
    Salva DataFrame em múltiplos formatos

    Args:
        df: DataFrame a salvar
        base_path: Diretório base
        base_filename: Nome base do arquivo (sem extensão)
        formatos: Lista de formatos ('csv', 'parquet', 'json')

    Returns:
        Dicionário com caminhos dos arquivos salvos
    """
    caminhos = {}

    if "csv" in formatos:
        caminho = f"{base_path}/{base_filename}.csv"
        df.to_csv(caminho, index=False)
        caminhos["csv"] = caminho
        print(f"✅ CSV salvo: {caminho}")

    if "parquet" in formatos:
        caminho = f"{base_path}/{base_filename}.parquet"
        df.to_parquet(caminho, index=False, engine="pyarrow")
        caminhos["parquet"] = caminho
        print(f"✅ Parquet salvo: {caminho}")

    if "json" in formatos:
        caminho = f"{base_path}/{base_filename}.json"
        df.to_json(caminho, orient="records", lines=True)
        caminhos["json"] = caminho
        print(f"✅ JSON salvo: {caminho}")

    return caminhos


def calcular_metricas_financeiras(
    df: pd.DataFrame, coluna_churn: str = "Churn_Binary"
) -> Dict:
    """
    Calcula métricas financeiras relacionadas ao churn

    Args:
        df: DataFrame com dados
        coluna_churn: Nome da coluna binária de churn

    Returns:
        Dicionário com métricas financeiras
    """
    churned = df[df[coluna_churn] == 1]

    metricas = {
        "receita_mensal_perdida": churned["MonthlyCharges"].sum(),
        "receita_total_perdida": churned["TotalCharges"].sum(),
        "ticket_medio_churn": churned["MonthlyCharges"].mean(),
        "ticket_medio_ativo": df[df[coluna_churn] == 0]["MonthlyCharges"].mean(),
    }

    return {k: round(v, 2) for k, v in metricas.items()}


def criar_resumo_execucao(inicio: datetime, fim: datetime, metricas: Dict) -> str:
    """
    Cria resumo da execução do pipeline

    Args:
        inicio: Timestamp de início
        fim: Timestamp de fim
        metricas: Métricas da execução

    Returns:
        String com resumo formatado
    """
    duracao = (fim - inicio).total_seconds()

    resumo = f"""
{'='*60}
RESUMO DA EXECUÇÃO DO PIPELINE
{'='*60}
Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}
Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}
Duração: {duracao:.2f} segundos

MÉTRICAS:
"""

    for chave, valor in metricas.items():
        resumo += f"  - {chave}: {valor}\n"

    resumo += f"\n{'='*60}\n"

    return resumo


def verificar_qualidade_features(df: pd.DataFrame, features: List[str]) -> Dict:
    """
    Verifica qualidade das features criadas

    Args:
        df: DataFrame com features
        features: Lista de features para verificar

    Returns:
        Dicionário com estatísticas de qualidade
    """
    qualidade = {}

    for feature in features:
        if feature not in df.columns:
            qualidade[feature] = {"erro": "Feature não encontrada"}
            continue

        qualidade[feature] = {
            "tipo": str(df[feature].dtype),
            "ausentes": int(df[feature].isnull().sum()),
            "unicos": int(df[feature].nunique()),
            "min": (
                float(df[feature].min())
                if pd.api.types.is_numeric_dtype(df[feature])
                else None
            ),
            "max": (
                float(df[feature].max())
                if pd.api.types.is_numeric_dtype(df[feature])
                else None
            ),
            "media": (
                float(df[feature].mean())
                if pd.api.types.is_numeric_dtype(df[feature])
                else None
            ),
        }

    return qualidade


def log_progresso(mensagem: str, nivel: str = "INFO") -> None:
    """
    Imprime mensagem de progresso formatada

    Args:
        mensagem: Mensagem a imprimir
        nivel: Nível do log (INFO, SUCCESS, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    simbolos = {"INFO": "📝", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}

    simbolo = simbolos.get(nivel, "📝")
    print(f"[{timestamp}] {simbolo} {mensagem}")


# Constantes úteis
COLUNAS_OBRIGATORIAS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]

SERVICOS = [
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]
