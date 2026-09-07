import pandas as pd

arquivo = "dados_originais/acidentes2026_todas_causas_tipos.csv"

print("Lendo o arquivo...")

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    low_memory=False
)

print("\n===== INFORMAÇÕES DO ARQUIVO =====")
print(f"Linhas: {len(df):,}")
print(f"Colunas: {len(df.columns)}")

print("\n===== COLUNAS =====")
for coluna in df.columns:
    print(coluna)

print("\n===== PRIMEIRAS 5 LINHAS =====")
print(df.head())

print("\n===== ACIDENTES DISTINTOS =====")
print(df["id"].nunique())