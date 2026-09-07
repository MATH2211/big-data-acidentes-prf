import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO
# ============================================================

arquivo = Path("dados_tratados/acidentes_2020_2026.csv")

print("=" * 60)
print("VALIDAÇÃO FINAL DA BASE CONSOLIDADA")
print("=" * 60)

# ============================================================
# LEITURA
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
# 1. TAMANHO DA BASE
# ============================================================

print("\n" + "=" * 60)
print("1. TAMANHO DA BASE")
print("=" * 60)

print(f"Registros: {len(df):,}")
print(f"Colunas: {len(df.columns)}")

# ============================================================
# 2. COLUNAS
# ============================================================

print("\n" + "=" * 60)
print("2. COLUNAS")
print("=" * 60)

for coluna in df.columns:
    print(f"- {coluna}")

# ============================================================
# 3. ACIDENTES DISTINTOS
# ============================================================

print("\n" + "=" * 60)
print("3. ACIDENTES DISTINTOS")
print("=" * 60)

total_acidentes = df["ID_ACIDENTE"].nunique()

print(f"Acidentes distintos: {total_acidentes:,}")

# ============================================================
# 4. ACIDENTES POR ANO
# ============================================================

print("\n" + "=" * 60)
print("4. ACIDENTES DISTINTOS POR ANO")
print("=" * 60)

acidentes_por_ano = (
    df.groupby("ANO")["ID_ACIDENTE"]
    .nunique()
)

for ano, quantidade in acidentes_por_ano.items():
    print(f"{ano}: {quantidade:,}")

# ============================================================
# 5. REGISTROS POR ANO
# ============================================================

print("\n" + "=" * 60)
print("5. REGISTROS POR ANO")
print("=" * 60)

registros_por_ano = df["ANO"].value_counts().sort_index()

for ano, quantidade in registros_por_ano.items():
    print(f"{ano}: {quantidade:,}")

# ============================================================
# 6. PERÍODO
# ============================================================

print("\n" + "=" * 60)
print("6. PERÍODO DA BASE")
print("=" * 60)

df["DATA"] = pd.to_datetime(
    df["DATA"],
    errors="coerce"
)

print(f"Data inicial: {df['DATA'].min().date()}")
print(f"Data final:   {df['DATA'].max().date()}")

datas_invalidas = df["DATA"].isna().sum()

print(f"Datas inválidas: {datas_invalidas}")

# ============================================================
# 7. VALORES AUSENTES
# ============================================================

print("\n" + "=" * 60)
print("7. VALORES AUSENTES POR COLUNA")
print("=" * 60)

ausentes = df.isna().sum()

for coluna, quantidade in ausentes.items():
    percentual = (quantidade / len(df)) * 100
    print(f"{coluna:25} {quantidade:10,} ({percentual:6.2f}%)")

# ============================================================
# 8. DUPLICIDADE DO ID
# ============================================================

print("\n" + "=" * 60)
print("8. DUPLICIDADE DOS IDS")
print("=" * 60)

registros_duplicados_id = df["ID_ACIDENTE"].duplicated().sum()

print(
    f"Registros que possuem ID_ACIDENTE repetido: "
    f"{registros_duplicados_id:,}"
)

print(
    "\nOBS: IDs repetidos são esperados, pois a base possui "
    "mais de um registro para determinados acidentes."
)

# ============================================================
# 9. CAUSAS
# ============================================================

print("\n" + "=" * 60)
print("9. CAUSAS")
print("=" * 60)

print(f"Quantidade de causas: {df['CAUSA'].nunique()}")

print("\n10 principais causas:")

print(
    df["CAUSA"]
    .value_counts()
    .head(10)
    .to_string()
)

# ============================================================
# 10. GRAVIDADE
# ============================================================

print("\n" + "=" * 60)
print("10. GRAVIDADE")
print("=" * 60)

print(
    df["GRAVIDADE"]
    .value_counts(dropna=False)
    .to_string()
)

# ============================================================
# 11. CONDIÇÃO METEOROLÓGICA
# ============================================================

print("\n" + "=" * 60)
print("11. CONDIÇÃO METEOROLÓGICA")
print("=" * 60)

print(
    df["CONDICAO_METEOROLOGICA"]
    .value_counts(dropna=False)
    .to_string()
)

# ============================================================
# 12. TIPO DE PISTA
# ============================================================

print("\n" + "=" * 60)
print("12. TIPO DE PISTA")
print("=" * 60)

print(
    df["TIPO_DE_PISTA"]
    .value_counts(dropna=False)
    .to_string()
)

# ============================================================
# 13. VEÍCULOS
# ============================================================

print("\n" + "=" * 60)
print("13. VEÍCULOS")
print("=" * 60)

print(
    df["VEICULO"]
    .value_counts(dropna=False)
    .head(20)
    .to_string()
)

# ============================================================
# 14. ESTADO FÍSICO
# ============================================================

print("\n" + "=" * 60)
print("14. ESTADO FÍSICO")
print("=" * 60)

print(
    df["ESTADO_FISICO"]
    .value_counts(dropna=False)
    .to_string()
)

# ============================================================
# 15. VALIDAÇÃO DOS CAMPOS NUMÉRICOS
# ============================================================

print("\n" + "=" * 60)
print("15. CAMPOS NUMÉRICOS")
print("=" * 60)

campos_numericos = [
    "KM",
    "ILESOS",
    "FERIDOS_LEVES",
    "FERIDOS_GRAVES",
    "MORTOS"
]

for coluna in campos_numericos:

    negativos = (df[coluna] < 0).sum()

    print(
        f"{coluna:20} "
        f"mínimo={df[coluna].min()} | "
        f"máximo={df[coluna].max()} | "
        f"negativos={negativos}"
    )

# ============================================================
# 16. VERIFICAÇÃO DOS ANOS
# ============================================================

print("\n" + "=" * 60)
print("16. ANOS PRESENTES")
print("=" * 60)

print(
    sorted(df["ANO"].dropna().unique().tolist())
)

# ============================================================
# 17. MESES PRESENTES POR ANO
# ============================================================

print("\n" + "=" * 60)
print("17. MESES PRESENTES POR ANO")
print("=" * 60)

df["MES"] = df["DATA"].dt.month

for ano in sorted(df["ANO"].dropna().unique()):

    meses = sorted(
        df.loc[df["ANO"] == ano, "MES"]
        .dropna()
        .unique()
        .tolist()
    )

    print(f"{int(ano)}: {meses}")

# ============================================================
# RESULTADO FINAL
# ============================================================

print("\n" + "=" * 60)
print("VALIDAÇÃO FINAL CONCLUÍDA")
print("=" * 60)

print("\nA base está pronta para a etapa de análise exploratória.")
print("Arquivo analisado:")
print(arquivo)