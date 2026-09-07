import pandas as pd
from pathlib import Path


# ==========================================
# CONFIGURAÇÕES
# ==========================================

PASTA_TRATADOS = Path("dados_tratados")

ARQUIVO_SAIDA = (
    PASTA_TRATADOS /
    "acidentes_2020_2026.csv"
)


# ==========================================
# LOCALIZAR ARQUIVOS
# ==========================================

arquivos = sorted(
    PASTA_TRATADOS.glob("acidentes*_tratado.csv")
)

print("==========================================")
print("CONSOLIDAÇÃO DAS BASES DA PRF")
print("==========================================")

print(
    f"Arquivos encontrados: {len(arquivos)}"
)


if not arquivos:
    print("\nNenhum arquivo tratado encontrado.")
    raise SystemExit


# ==========================================
# LISTA PARA ARMAZENAR OS DATAFRAMES
# ==========================================

dataframes = []


# ==========================================
# LER CADA ARQUIVO
# ==========================================

for arquivo in arquivos:

    print("\n------------------------------------------")
    print(f"Lendo: {arquivo.name}")
    print("------------------------------------------")

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    print(
        f"Linhas: {len(df):,}"
    )

    # --------------------------------------
    # IDENTIFICAR O ANO
    # --------------------------------------

    df["DATA"] = pd.to_datetime(
        df["DATA"],
        errors="coerce"
    )

    df["ANO"] = df["DATA"].dt.year

    dataframes.append(df)


# ==========================================
# CONSOLIDAR
# ==========================================

print("\n==========================================")
print("JUNTANDO OS ARQUIVOS")
print("==========================================")

df_final = pd.concat(
    dataframes,
    ignore_index=True
)


# ==========================================
# ORDENAR
# ==========================================

df_final = df_final.sort_values(
    by=["DATA", "ID_ACIDENTE"]
).reset_index(drop=True)


# ==========================================
# SALVAR
# ==========================================

print("\nSalvando base consolidada...")

df_final.to_csv(
    ARQUIVO_SAIDA,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# VALIDAÇÃO
# ==========================================

print("\n==========================================")
print("VALIDAÇÃO DA BASE CONSOLIDADA")
print("==========================================")

print(
    f"Linhas totais: "
    f"{len(df_final):,}"
)

print(
    f"Colunas totais: "
    f"{len(df_final.columns)}"
)

print(
    f"Acidentes distintos: "
    f"{df_final['ID_ACIDENTE'].nunique():,}"
)

print(
    f"Data mínima: "
    f"{df_final['DATA'].min()}"
)

print(
    f"Data máxima: "
    f"{df_final['DATA'].max()}"
)

print(
    f"Anos encontrados: "
    f"{df_final['ANO'].nunique()}"
)


# ==========================================
# REGISTROS POR ANO
# ==========================================

print("\n==========================================")
print("REGISTROS POR ANO")
print("==========================================")

print(
    df_final["ANO"]
    .value_counts()
    .sort_index()
    .to_string()
)


# ==========================================
# ACIDENTES DISTINTOS POR ANO
# ==========================================

print("\n==========================================")
print("ACIDENTES DISTINTOS POR ANO")
print("==========================================")

acidentes_por_ano = (
    df_final
    .groupby("ANO")["ID_ACIDENTE"]
    .nunique()
)

print(
    acidentes_por_ano
    .to_string()
)


# ==========================================
# VERIFICAR IDs DUPLICADOS ENTRE ANOS
# ==========================================

print("\n==========================================")
print("VERIFICAÇÃO DOS IDs")
print("==========================================")

ids_por_ano = (
    df_final
    .groupby("ID_ACIDENTE")["ANO"]
    .nunique()
)

ids_em_mais_de_um_ano = (
    ids_por_ano > 1
).sum()

print(
    f"IDs presentes em mais de um ano: "
    f"{ids_em_mais_de_um_ano:,}"
)


# ==========================================
# ARQUIVO
# ==========================================

print("\n==========================================")
print("CONSOLIDAÇÃO CONCLUÍDA")
print("==========================================")

print(
    f"Arquivo criado: "
    f"{ARQUIVO_SAIDA}"
)