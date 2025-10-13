"""
transformacao.py
Script para transformação de dados - Camada Silver
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings("ignore")

# Importar funções utilitárias
from utils import (
    imprimir_separador,
    log_progresso,
    salvar_dataframe_multiplos_formatos,
    comparar_tamanhos_arquivo,
    gerar_relatorio_texto,
    verificar_qualidade_features,
    SERVICOS,
)


class TransformadorDados:
    """
    Classe responsável pela transformação e engenharia de features
    """

    def __init__(self, caminho_base: str = "/content/dados"):
        """
        Inicializa o transformador

        Args:
            caminho_base: Diretório base dos dados
        """
        self.caminho_base = caminho_base
        self.caminho_bronze = f"{caminho_base}/bronze"
        self.caminho_silver = f"{caminho_base}/silver"
        self.caminho_gold = f"{caminho_base}/gold"
        self.timestamp_inicio = datetime.now()
        self.features_criadas = []

    def carregar_bronze(
        self, nome_arquivo: str = "telco_churn_raw.csv"
    ) -> pd.DataFrame:
        """
        Carrega dados da camada Bronze

        Args:
            nome_arquivo: Nome do arquivo a carregar

        Returns:
            DataFrame com dados brutos
        """
        imprimir_separador("CARREGANDO DADOS DA CAMADA BRONZE")

        caminho = f"{self.caminho_bronze}/{nome_arquivo}"

        try:
            df = pd.read_csv(caminho)
            log_progresso(f"✅ {len(df):,} registros carregados", "SUCCESS")
            return df
        except FileNotFoundError:
            log_progresso(f"Arquivo não encontrado: {caminho}", "ERROR")
            raise

    def limpar_dados(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Realiza limpeza dos dados

        Args:
            df: DataFrame a limpar

        Returns:
            DataFrame limpo
        """
        imprimir_separador("LIMPEZA DE DADOS")

        df_limpo = df.copy()

        # 1. Converter TotalCharges para numérico
        log_progresso("Convertendo TotalCharges para numérico...", "INFO")
        df_limpo["TotalCharges"] = pd.to_numeric(
            df_limpo["TotalCharges"], errors="coerce"
        )
        valores_vazios = df_limpo["TotalCharges"].isnull().sum()
        log_progresso(f"Valores vazios encontrados: {valores_vazios}", "INFO")

        # 2. Tratar valores ausentes
        log_progresso("Tratando valores ausentes...", "INFO")

        # Clientes novos com tenure=0
        df_limpo.loc[df_limpo["tenure"] == 0, "TotalCharges"] = 0

        # Clientes com tenure > 0 mas TotalCharges NaN
        mask = (df_limpo["TotalCharges"].isnull()) & (df_limpo["tenure"] > 0)
        df_limpo.loc[mask, "TotalCharges"] = (
            df_limpo.loc[mask, "MonthlyCharges"] * df_limpo.loc[mask, "tenure"]
        )

        log_progresso(f"Valores preenchidos: {valores_vazios}", "SUCCESS")

        # 3. Remover duplicatas
        duplicatas_antes = df_limpo.duplicated(subset="customerID").sum()
        df_limpo = df_limpo.drop_duplicates(subset="customerID", keep="first")
        log_progresso(f"Duplicatas removidas: {duplicatas_antes}", "SUCCESS")

        # 4. Verificar resultado
        ausentes_final = df_limpo.isnull().sum().sum()
        log_progresso(f"Valores ausentes após limpeza: {ausentes_final}", "SUCCESS")

        return df_limpo

    def criar_feature_churn_binary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria feature binária de churn
        """
        df["Churn_Binary"] = (df["Churn"] == "Yes").astype(int)
        self.features_criadas.append("Churn_Binary")
        return df

    def criar_feature_avg_charge(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria feature de valor médio mensal
        """
        df["AvgChargePerMonth"] = df["TotalCharges"] / (df["tenure"] + 1)
        self.features_criadas.append("AvgChargePerMonth")
        return df

    def criar_feature_tenure_group(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categoriza tenure em grupos
        """

        def categorizar(tenure):
            if tenure <= 12:
                return "Novo"
            elif tenure <= 36:
                return "Medio"
            else:
                return "Longo"

        df["TenureGroup"] = df["tenure"].apply(categorizar)
        self.features_criadas.append("TenureGroup")
        return df

    def criar_feature_is_premium(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria flag de cliente premium
        """
        mediana = df["MonthlyCharges"].median()
        df["IsPremium"] = (df["MonthlyCharges"] > mediana).astype(int)
        self.features_criadas.append("IsPremium")
        return df

    def criar_feature_num_servicos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Conta total de serviços contratados
        """

        def contar_servicos(row):
            count = 0
            for servico in SERVICOS:
                if servico in row.index:
                    valor = row[servico]
                    if valor not in [
                        "No",
                        "No phone service",
                        "No internet service",
                        pd.NA,
                        None,
                    ]:
                        count += 1
            return count

        df["NumServicos"] = df.apply(contar_servicos, axis=1)
        self.features_criadas.append("NumServicos")
        return df

    def criar_feature_has_security(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria flag de serviços de segurança
        """
        df["HasSecurity"] = (
            (df["OnlineSecurity"] == "Yes") | (df["DeviceProtection"] == "Yes")
        ).astype(int)
        self.features_criadas.append("HasSecurity")
        return df

    def criar_feature_satisfaction_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula score de satisfação estimado
        """
        df["SatisfactionScore"] = (
            (df["Contract"] != "Month-to-month").astype(int) * 3
            + (df["NumServicos"] / df["NumServicos"].max()) * 3
            + (df["TechSupport"] == "Yes").astype(int) * 2
            + (df["tenure"] / df["tenure"].max()) * 2
        )
        self.features_criadas.append("SatisfactionScore")
        return df

    def criar_feature_churn_risk_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula score de risco de churn
        """
        mediana_charges = df["MonthlyCharges"].median()

        df["ChurnRiskScore"] = (
            (df["Contract"] == "Month-to-month").astype(int) * 3
            + (df["tenure"] < 12).astype(int) * 2
            + (df["NumServicos"] <= 2).astype(int) * 2
            + (df["HasSecurity"] == 0).astype(int) * 1
            + (df["MonthlyCharges"] > mediana_charges).astype(int) * 1
        )
        self.features_criadas.append("ChurnRiskScore")
        return df

    def normalizar_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza features numéricas
        """
        log_progresso("Normalizando features...", "INFO")

        scaler = MinMaxScaler()

        df["MonthlyCharges_Normalized"] = scaler.fit_transform(df[["MonthlyCharges"]])
        df["TotalCharges_Normalized"] = scaler.fit_transform(df[["TotalCharges"]])

        self.features_criadas.extend(
            ["MonthlyCharges_Normalized", "TotalCharges_Normalized"]
        )

        log_progresso("Features normalizadas (escala 0-1)", "SUCCESS")

        return df

    def aplicar_engenharia_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica todas as transformações de engenharia de features

        Args:
            df: DataFrame limpo

        Returns:
            DataFrame com features criadas
        """
        imprimir_separador("ENGENHARIA DE FEATURES")

        df_transformed = df.copy()

        # Aplicar cada transformação
        log_progresso("Criando Churn_Binary...", "INFO")
        df_transformed = self.criar_feature_churn_binary(df_transformed)

        log_progresso("Criando AvgChargePerMonth...", "INFO")
        df_transformed = self.criar_feature_avg_charge(df_transformed)

        log_progresso("Criando TenureGroup...", "INFO")
        df_transformed = self.criar_feature_tenure_group(df_transformed)

        log_progresso("Criando IsPremium...", "INFO")
        df_transformed = self.criar_feature_is_premium(df_transformed)

        log_progresso("Criando NumServicos...", "INFO")
        df_transformed = self.criar_feature_num_servicos(df_transformed)

        log_progresso("Criando HasSecurity...", "INFO")
        df_transformed = self.criar_feature_has_security(df_transformed)

        log_progresso("Criando SatisfactionScore...", "INFO")
        df_transformed = self.criar_feature_satisfaction_score(df_transformed)

        log_progresso("Criando ChurnRiskScore...", "INFO")
        df_transformed = self.criar_feature_churn_risk_score(df_transformed)

        log_progresso("Normalizando features...", "INFO")
        df_transformed = self.normalizar_features(df_transformed)

        log_progresso(f"✅ {len(self.features_criadas)} features criadas", "SUCCESS")

        return df_transformed

    def validar_transformacao(
        self, df_original: pd.DataFrame, df_transformado: pd.DataFrame
    ) -> Dict:
        """
        Valida a qualidade da transformação

        Args:
            df_original: DataFrame original
            df_transformado: DataFrame transformado

        Returns:
            Dicionário com métricas de validação
        """
        imprimir_separador("VALIDAÇÃO DA TRANSFORMAÇÃO")

        metricas = {
            "registros_antes": len(df_original),
            "registros_depois": len(df_transformado),
            "colunas_antes": len(df_original.columns),
            "colunas_depois": len(df_transformado.columns),
            "features_criadas": len(self.features_criadas),
            "valores_ausentes": df_transformado.isnull().sum().sum(),
        }

        log_progresso(
            f"Registros: {metricas['registros_antes']:,} → {metricas['registros_depois']:,}",
            "INFO",
        )
        log_progresso(
            f"Colunas: {metricas['colunas_antes']} → {metricas['colunas_depois']}",
            "INFO",
        )
        log_progresso(f"Features criadas: {metricas['features_criadas']}", "SUCCESS")
        log_progresso(f"Valores ausentes: {metricas['valores_ausentes']}", "INFO")

        # Verificar qualidade das features criadas
        qualidade = verificar_qualidade_features(df_transformado, self.features_criadas)

        return metricas

    def salvar_silver(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Salva dados na camada Silver

        Args:
            df: DataFrame transformado

        Returns:
            Dicionário com caminhos dos arquivos
        """
        imprimir_separador("SALVANDO NA CAMADA SILVER")

        caminhos = salvar_dataframe_multiplos_formatos(
            df=df,
            base_path=self.caminho_silver,
            base_filename="telco_churn_transformed",
            formatos=["csv", "parquet"],
        )

        # Comparar tamanhos
        comparacao = comparar_tamanhos_arquivo(caminhos["csv"], caminhos["parquet"])

        log_progresso(
            f"CSV: {comparacao['csv_mb']} MB | Parquet: {comparacao['parquet_mb']} MB | "
            f"Redução: {comparacao['reducao_percentual']}%",
            "SUCCESS",
        )

        return caminhos

    def criar_datasets_gold(self, df: pd.DataFrame) -> None:
        """
        Cria datasets agregados para a camada Gold

        Args:
            df: DataFrame transformado
        """
        imprimir_separador("CRIANDO DATASETS GOLD")

        # Dataset 1: Métricas por contrato
        log_progresso("Criando métricas por contrato...", "INFO")
        df_contract = (
            df.groupby("Contract")
            .agg(
                {
                    "customerID": "count",
                    "Churn_Binary": ["sum", "mean"],
                    "MonthlyCharges": ["mean", "median"],
                    "TotalCharges": ["mean", "median"],
                    "tenure": ["mean", "median"],
                    "NumServicos": "mean",
                    "SatisfactionScore": "mean",
                }
            )
            .round(2)
        )

        df_contract.columns = [
            "_".join(col).strip() for col in df_contract.columns.values
        ]
        df_contract.reset_index(inplace=True)
        df_contract.to_csv(
            f"{self.caminho_gold}/metricas_por_contrato.csv", index=False
        )
        log_progresso("✅ metricas_por_contrato.csv", "SUCCESS")

        # Dataset 2: Análise por segmento
        log_progresso("Criando análise por segmento...", "INFO")
        df_segments = (
            df.groupby(["TenureGroup", "IsPremium"])
            .agg(
                {
                    "customerID": "count",
                    "Churn_Binary": ["sum", "mean"],
                    "SatisfactionScore": "mean",
                    "NumServicos": "mean",
                }
            )
            .round(2)
        )

        df_segments.columns = [
            "_".join(col).strip() for col in df_segments.columns.values
        ]
        df_segments.reset_index(inplace=True)
        df_segments.to_csv(f"{self.caminho_gold}/churn_por_segmento.csv", index=False)
        log_progresso("✅ churn_por_segmento.csv", "SUCCESS")

        # Dataset 3: Perfil alto risco
        log_progresso("Criando perfil de alto risco...", "INFO")
        df_alto_risco = df[df["Churn_Binary"] == 1]
        df_alto_risco_summary = df_alto_risco.describe().T
        df_alto_risco_summary.to_csv(f"{self.caminho_gold}/perfil_alto_risco.csv")
        log_progresso("✅ perfil_alto_risco.csv", "SUCCESS")

        # Dataset 4: Correlações
        log_progresso("Criando análise de correlações...", "INFO")
        numeric_cols = [
            "tenure",
            "MonthlyCharges",
            "TotalCharges",
            "NumServicos",
            "SatisfactionScore",
            "IsPremium",
            "HasSecurity",
            "ChurnRiskScore",
        ]
        correlations = (
            df[numeric_cols + ["Churn_Binary"]]
            .corr()["Churn_Binary"]
            .sort_values(ascending=False)
        )

        correlations_df = pd.DataFrame(
            {"Feature": correlations.index, "Correlation": correlations.values}
        )
        correlations_df.to_csv(
            f"{self.caminho_gold}/correlacoes_churn.csv", index=False
        )
        log_progresso("✅ correlacoes_churn.csv", "SUCCESS")

    def gerar_relatorio(self, metricas: Dict) -> None:
        """
        Gera relatório de transformação

        Args:
            metricas: Métricas da transformação
        """
        caminho_relatorio = f"{self.caminho_silver}/relatorio_transformacao.txt"

        tempo_execucao = (datetime.now() - self.timestamp_inicio).total_seconds()

        metricas_relatorio = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Registros Processados": metricas.get("registros_depois", 0),
            "Features Originais": metricas.get("colunas_antes", 0),
            "Features Após Engenharia": metricas.get("colunas_depois", 0),
            "Novas Features": metricas.get("features_criadas", 0),
            "Features Criadas": ", ".join(self.features_criadas),
            "Valores Ausentes": metricas.get("valores_ausentes", 0),
            "Tempo de Execução": f"{tempo_execucao:.2f}s",
        }

        gerar_relatorio_texto(
            titulo="RELATÓRIO DE TRANSFORMAÇÃO",
            metricas=metricas_relatorio,
            caminho_output=caminho_relatorio,
        )

    def executar_pipeline_completo(self) -> pd.DataFrame:
        """
        Executa pipeline completo de transformação

        Returns:
            DataFrame transformado
        """
        imprimir_separador("🚀 INICIANDO PIPELINE DE TRANSFORMAÇÃO", caractere="=")

        # 1. Carregar dados Bronze
        df_bronze = self.carregar_bronze()
        df_original_shape = df_bronze.shape

        # 2. Limpar dados
        df_limpo = self.limpar_dados(df_bronze)

        # 3. Aplicar engenharia de features
        df_transformado = self.aplicar_engenharia_features(df_limpo)

        # 4. Validar transformação
        metricas = self.validar_transformacao(df_bronze, df_transformado)

        # 5. Salvar na camada Silver
        self.salvar_silver(df_transformado)

        # 6. Criar datasets Gold
        self.criar_datasets_gold(df_transformado)

        # 7. Gerar relatório
        self.gerar_relatorio(metricas)

        imprimir_separador("✅ TRANSFORMAÇÃO COMPLETA", caractere="=")

        tempo_total = (datetime.now() - self.timestamp_inicio).total_seconds()
        log_progresso(f"Tempo total: {tempo_total:.2f}s", "SUCCESS")

        return df_transformado


def main():
    """
    Função principal para execução standalone
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Transformação de dados - Camada Silver"
    )
    parser.add_argument(
        "--base-path",
        type=str,
        default="/content/dados",
        help="Diretório base dos dados",
    )

    args = parser.parse_args()

    # Executar pipeline
    transformador = TransformadorDados(caminho_base=args.base_path)
    df_transformado = transformador.executar_pipeline_completo()

    print(f"\n✅ Pipeline concluído. {len(df_transformado):,} registros transformados.")
    print(f"✅ {len(transformador.features_criadas)} features criadas.")


if __name__ == "__main__":
    main()


# Exemplo de uso no Colab:
"""
# No Google Colab, após executar a ingestão:

from src.transformacao import TransformadorDados

# Criar transformador
transformador = TransformadorDados(caminho_base='/content/dados')

# Executar pipeline completo
df_silver = transformador.executar_pipeline_completo()

# Ou executar etapas individualmente:
df_bronze = transformador.carregar_bronze()
df_limpo = transformador.limpar_dados(df_bronze)
df_transformed = transformador.aplicar_engenharia_features(df_limpo)
transformador.salvar_silver(df_transformed)
transformador.criar_datasets_gold(df_transformed)
"""
