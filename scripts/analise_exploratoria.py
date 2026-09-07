import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO
# ============================================================

arquivo = Path("dados_tratados/acidentes_2020_2026.csv")

print("=" * 70)
print("ANÁLISE EXPLORATÓRIA — CAUSAS E GRAVIDADE")
print("=" * 70)

# ============================================================
# LEITURA DA BASE
# ============================================================

print("\nLendo a base...")

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="utf-8-sig",
    low_memory=False
)

print("Base carregada com sucesso!")

# ============================================================
# PREPARAÇÃO
# ============================================================

df["DATA"] = pd.to_datetime(
    df["DATA"],
    errors="coerce"
)

# ============================================================
# 1. VISÃO GERAL
# ============================================================

print("\n" + "=" * 70)
print("1. VISÃO GERAL")
print("=" * 70)

print(f"Registros: {len(df):,}")
print(f"Acidentes distintos: {df['ID_ACIDENTE'].nunique():,}")
print(f"Data inicial: {df['DATA'].min().date()}")
print(f"Data final: {df['DATA'].max().date()}")

# ============================================================
# 2. PRINCIPAIS CAUSAS
# ============================================================

print("\n" + "=" * 70)
print("2. PRINCIPAIS CAUSAS DOS REGISTROS")
print("=" * 70)

principais_causas = (
    df["CAUSA"]
    .value_counts()
    .head(15)
)

print(principais_causas.to_string())

# ============================================================
# 3. GRAVIDADE
# ============================================================

print("\n" + "=" * 70)
print("3. DISTRIBUIÇÃO DA GRAVIDADE")
print("=" * 70)

gravidade = (
    df["GRAVIDADE"]
    .value_counts(dropna=False)
)

print(gravidade.to_string())

# ============================================================
# 4. CAUSAS X GRAVIDADE
# ============================================================

print("\n" + "=" * 70)
print("4. PRINCIPAIS CAUSAS POR GRAVIDADE")
print("=" * 70)

tabela_causa_gravidade = pd.crosstab(
    df["CAUSA"],
    df["GRAVIDADE"]
)

print("\nTop 15 causas por quantidade total:")

top_15 = (
    df["CAUSA"]
    .value_counts()
    .head(15)
    .index
)

print(
    tabela_causa_gravidade
    .loc[top_15]
    .to_string()
)

# ============================================================
# 5. PERCENTUAL DE ACIDENTES FATAIS POR CAUSA
# ============================================================

print("\n" + "=" * 70)
print("5. PERCENTUAL DE REGISTROS COM VÍTIMAS FATAIS POR CAUSA")
print("=" * 70)

# Criamos uma cópia apenas para esta análise
df_fatalidade = df.copy()

df_fatalidade["FATAL"] = (
    df_fatalidade["GRAVIDADE"] == "Com Vítimas Fatais"
)

analise_fatalidade = (
    df_fatalidade
    .groupby("CAUSA")
    .agg(
        REGISTROS=("ID_ACIDENTE", "size"),
        ACIDENTES=("ID_ACIDENTE", "nunique"),
        FATAIS=("FATAL", "sum")
    )
)

analise_fatalidade["PERCENTUAL_FATAL"] = (
    analise_fatalidade["FATAIS"]
    / analise_fatalidade["REGISTROS"]
    * 100
)

# Consideramos somente causas com pelo menos 100 registros
analise_fatalidade = analise_fatalidade[
    analise_fatalidade["REGISTROS"] >= 100
]

analise_fatalidade = (
    analise_fatalidade
    .sort_values("PERCENTUAL_FATAL", ascending=False)
)

print(
    analise_fatalidade
    .head(15)
    .to_string()
)

# ============================================================
# 6. MORTOS POR CAUSA
# ============================================================

print("\n" + "=" * 70)
print("6. MORTOS POR CAUSA")
print("=" * 70)

mortos_por_causa = (
    df.groupby("CAUSA")["MORTOS"]
    .sum()
    .sort_values(ascending=False)
)

print(
    mortos_por_causa
    .head(15)
    .to_string()
)

# ============================================================
# 7. FERIDOS GRAVES POR CAUSA
# ============================================================

print("\n" + "=" * 70)
print("7. FERIDOS GRAVES POR CAUSA")
print("=" * 70)

feridos_graves_por_causa = (
    df.groupby("CAUSA")["FERIDOS_GRAVES"]
    .sum()
    .sort_values(ascending=False)
)

print(
    feridos_graves_por_causa
    .head(15)
    .to_string()
)

# ============================================================
# 8. GRAVIDADE POR ANO
# ============================================================

print("\n" + "=" * 70)
print("8. GRAVIDADE POR ANO")
print("=" * 70)

gravidade_ano = pd.crosstab(
    df["ANO"],
    df["GRAVIDADE"]
)

print(
    gravidade_ano
    .to_string()
)

# ============================================================
# 9. PRINCIPAIS CAUSAS EM ACIDENTES FATAIS
# ============================================================

print("\n" + "=" * 70)
print("9. PRINCIPAIS CAUSAS NOS REGISTROS DE ACIDENTES FATAIS")
print("=" * 70)

df_fatais = df[
    df["GRAVIDADE"] == "Com Vítimas Fatais"
]

causas_fatais = (
    df_fatais["CAUSA"]
    .value_counts()
    .head(15)
)

print(causas_fatais.to_string())

# ============================================================
# 10. RESUMO
# ============================================================

print("\n" + "=" * 70)
print("10. RESUMO DA ANÁLISE")
print("=" * 70)

print(
    f"\nQuantidade de causas encontradas: "
    f"{df['CAUSA'].nunique()}"
)

print(
    f"Registros classificados como fatais: "
    f"{len(df_fatais):,}"
)

print(
    f"Acidentes distintos classificados como fatais: "
    f"{df_fatais['ID_ACIDENTE'].nunique():,}"
)

print("\nAnálise exploratória concluída.")