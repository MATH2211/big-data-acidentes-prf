import pandas as pd
from pathlib import Path

# ==========================================
# 1. CAMINHOS DOS ARQUIVOS
# ==========================================

arquivo_entrada = Path(
    "dados_originais/acidentes2026_todas_causas_tipos.csv"
)

arquivo_saida = Path(
    "dados_tratados/acidentes2026_tratado.csv"
)

# ==========================================
# 2. LEITURA DO ARQUIVO ORIGINAL
# ==========================================

print("Lendo arquivo original...")

df = pd.read_csv(
    arquivo_entrada,
    sep=";",
    encoding="latin1",
    low_memory=False
)

print(f"Linhas originais: {len(df):,}")
print(f"Colunas originais: {len(df.columns)}")

# ==========================================
# 3. SELECIONAR AS COLUNAS IMPORTANTES
# ==========================================

colunas = [
    "id",
    "data_inversa",
    "horario",
    "uf",
    "br",
    "km",
    "municipio",
    "causa_acidente",
    "classificacao_acidente",
    "condicao_metereologica",
    "tipo_pista",
    "tipo_veiculo",
    "estado_fisico",
    "ilesos",
    "feridos_leves",
    "feridos_graves",
    "mortos"
]

df = df[colunas].copy()

# ==========================================
# 4. RENOMEAR AS COLUNAS
# ==========================================

df.rename(columns={
    "id": "ID_ACIDENTE",
    "data_inversa": "DATA",
    "horario": "HORA",
    "uf": "ESTADO",
    "br": "RODOVIA",
    "km": "KM",
    "municipio": "MUNICÍPIO",
    "causa_acidente": "CAUSA",
    "classificacao_acidente": "GRAVIDADE",
    "condicao_metereologica": "CONDICAO_METEOROLOGICA",
    "tipo_pista": "TIPO_DE_PISTA",
    "tipo_veiculo": "VEICULO",
    "estado_fisico": "ESTADO_FISICO",
    "ilesos": "ILESOS",
    "feridos_leves": "FERIDOS_LEVES",
    "feridos_graves": "FERIDOS_GRAVES",
    "mortos": "MORTOS"
}, inplace=True)

# ==========================================
# 5. LIMPEZA DOS CAMPOS DE TEXTO
# ==========================================

colunas_texto = [
    "ID_ACIDENTE",
    "ESTADO",
    "RODOVIA",
    "MUNICÍPIO",
    "CAUSA",
    "GRAVIDADE",
    "CONDICAO_METEOROLOGICA",
    "TIPO_DE_PISTA",
    "VEICULO",
    "ESTADO_FISICO"
]

for coluna in colunas_texto:
    df[coluna] = (
        df[coluna]
        .astype("string")
        .str.strip()
    )

# ==========================================
# 6. TRATAMENTO DA DATA
# ==========================================

df["DATA"] = pd.to_datetime(
    df["DATA"],
    errors="coerce"
)

# ==========================================
# 7. TRATAMENTO DO HORÁRIO
# ==========================================

df["HORA"] = pd.to_datetime(
    df["HORA"],
    errors="coerce"
).dt.strftime("%H:%M:%S")

# ==========================================
# 8. CAMPOS NUMÉRICOS
# ==========================================

colunas_numericas = [
    "KM",
    "ILESOS",
    "FERIDOS_LEVES",
    "FERIDOS_GRAVES",
    "MORTOS"
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )

# ==========================================
# 9. CRIAR PASTA DE SAÍDA
# ==========================================

arquivo_saida.parent.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# 10. SALVAR ARQUIVO TRATADO
# ==========================================

df.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# 11. VALIDAÇÃO
# ==========================================

print("\n==========================================")
print("VALIDAÇÃO DA BASE TRATADA")
print("==========================================")

print(f"Linhas finais: {len(df):,}")

print(
    f"Colunas finais: {len(df.columns)}"
)

print(
    f"Acidentes distintos: "
    f"{df['ID_ACIDENTE'].nunique():,}"
)

print(
    f"Estados: "
    f"{df['ESTADO'].nunique()}"
)

print(
    f"Causas: "
    f"{df['CAUSA'].nunique()}"
)

print(
    f"Condições meteorológicas: "
    f"{df['CONDICAO_METEOROLOGICA'].nunique()}"
)

print(
    f"Gravidades: "
    f"{df['GRAVIDADE'].nunique()}"
)

print("\nColunas finais:")

for coluna in df.columns:
    print(f"- {coluna}")

print("\nArquivo criado com sucesso:")
print(arquivo_saida)