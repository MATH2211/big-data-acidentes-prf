import pandas as pd
from pathlib import Path

# ==========================================
# 1. ARQUIVO TRATADO
# ==========================================

arquivo = Path(
    "dados_tratados/acidentes2026_tratado.csv"
)

print("Lendo a base tratada...")

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="utf-8-sig",
    low_memory=False
)

# ==========================================
# 2. INFORMAÇÕES GERAIS
# ==========================================

print("\n==========================================")
print("INFORMAÇÕES GERAIS")
print("==========================================")

print(f"Linhas: {len(df):,}")
print(f"Colunas: {len(df.columns)}")
print(f"Acidentes distintos: {df['ID_ACIDENTE'].nunique():,}")

# ==========================================
# 3. VALORES VAZIOS
# ==========================================

print("\n==========================================")
print("VALORES VAZIOS")
print("==========================================")

vazios = df.isna().sum()

for coluna, quantidade in vazios.items():
    percentual = (quantidade / len(df)) * 100

    print(
        f"{coluna}: "
        f"{quantidade:,} "
        f"({percentual:.2f}%)"
    )

# ==========================================
# 4. DATAS
# ==========================================

print("\n==========================================")
print("DATAS")
print("==========================================")

df["DATA"] = pd.to_datetime(
    df["DATA"],
    errors="coerce"
)

print(f"Data mínima: {df['DATA'].min()}")
print(f"Data máxima: {df['DATA'].max()}")
print(
    f"Datas inválidas: "
    f"{df['DATA'].isna().sum():,}"
)

# ==========================================
# 5. HORÁRIOS
# ==========================================

print("\n==========================================")
print("HORÁRIOS")
print("==========================================")

print(
    f"Horários vazios: "
    f"{df['HORA'].isna().sum():,}"
)

print("\nExemplos de horários:")

print(
    df["HORA"]
    .dropna()
    .drop_duplicates()
    .head(20)
    .to_string(index=False)
)

# ==========================================
# 6. ESTADOS
# ==========================================

print("\n==========================================")
print("ESTADOS")
print("==========================================")

print(
    df["ESTADO"]
    .value_counts(dropna=False)
    .to_string()
)

# ==========================================
# 7. GRAVIDADE
# ==========================================

print("\n==========================================")
print("GRAVIDADE")
print("==========================================")

print(
    df["GRAVIDADE"]
    .value_counts(dropna=False)
    .to_string()
)

# ==========================================
# 8. CAUSAS
# ==========================================

print("\n==========================================")
print("PRINCIPAIS CAUSAS")
print("==========================================")

print(
    df["CAUSA"]
    .value_counts(dropna=False)
    .head(20)
    .to_string()
)

# ==========================================
# 9. CONDIÇÃO METEOROLÓGICA
# ==========================================

print("\n==========================================")
print("CONDIÇÃO METEOROLÓGICA")
print("==========================================")

print(
    df["CONDICAO_METEOROLOGICA"]
    .value_counts(dropna=False)
    .to_string()
)

# ==========================================
# 10. VEÍCULOS
# ==========================================

print("\n==========================================")
print("PRINCIPAIS VEÍCULOS")
print("==========================================")

print(
    df["VEICULO"]
    .value_counts(dropna=False)
    .head(20)
    .to_string()
)

# ==========================================
# 11. VALORES NUMÉRICOS
# ==========================================

print("\n==========================================")
print("DADOS NUMÉRICOS")
print("==========================================")

colunas_numericas = [
    "KM",
    "ILESOS",
    "FERIDOS_LEVES",
    "FERIDOS_GRAVES",
    "MORTOS"
]

for coluna in colunas_numericas:

    print(f"\n--- {coluna} ---")

    print(f"Mínimo: {df[coluna].min()}")
    print(f"Máximo: {df[coluna].max()}")
    print(f"Soma: {df[coluna].sum()}")
    print(f"Vazios: {df[coluna].isna().sum():,}")

# ==========================================
# 12. FINAL
# ==========================================

print("\n==========================================")
print("AUDITORIA CONCLUÍDA")
print("==========================================")