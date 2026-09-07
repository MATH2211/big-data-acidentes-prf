import pandas as pd
from pathlib import Path


# ==========================================
# CONFIGURAÇÕES
# ==========================================

PASTA_ORIGINAIS = Path("dados_originais")
PASTA_TRATADOS = Path("dados_tratados")

PASTA_TRATADOS.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# COLUNAS QUE VAMOS MANTER
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


# ==========================================
# NOVOS NOMES DAS COLUNAS
# ==========================================

renomear = {
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
}


# ==========================================
# COLUNAS DE TEXTO
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


# ==========================================
# COLUNAS NUMÉRICAS
# ==========================================

colunas_numericas = [
    "KM",
    "ILESOS",
    "FERIDOS_LEVES",
    "FERIDOS_GRAVES",
    "MORTOS"
]


# ==========================================
# BUSCAR OS ARQUIVOS ORIGINAIS
# ==========================================

arquivos = sorted(
    PASTA_ORIGINAIS.glob("acidentes*_todas_causas_tipos.csv")
)

print("==========================================")
print("TRATAMENTO DOS ARQUIVOS DA PRF")
print("==========================================")
print(f"Arquivos encontrados: {len(arquivos)}")


if not arquivos:
    print("\nNenhum arquivo encontrado.")
    raise SystemExit


# ==========================================
# PROCESSAR CADA ARQUIVO
# ==========================================

for arquivo_entrada in arquivos:

    print("\n------------------------------------------")
    print(f"Processando: {arquivo_entrada.name}")
    print("------------------------------------------")

    try:

        # ----------------------------------
        # LEITURA
        # ----------------------------------

        df = pd.read_csv(
            arquivo_entrada,
            sep=";",
            encoding="latin1",
            low_memory=False
        )

        print(f"Linhas originais: {len(df):,}")
        print(f"Colunas originais: {len(df.columns)}")


        # ----------------------------------
        # VERIFICAR COLUNAS
        # ----------------------------------

        colunas_faltantes = [
            coluna
            for coluna in colunas
            if coluna not in df.columns
        ]

        if colunas_faltantes:

            print("\nERRO: colunas não encontradas:")
            for coluna in colunas_faltantes:
                print(f"- {coluna}")

            print("Arquivo ignorado.")
            continue


        # ----------------------------------
        # SELECIONAR COLUNAS
        # ----------------------------------

        df = df[colunas].copy()


        # ----------------------------------
        # RENOMEAR
        # ----------------------------------

        df.rename(
            columns=renomear,
            inplace=True
        )


        # ----------------------------------
        # LIMPEZA DOS TEXTOS
        # ----------------------------------

        for coluna in colunas_texto:

            df[coluna] = (
                df[coluna]
                .astype("string")
                .str.strip()
            )


        # ----------------------------------
        # DATA
        # ----------------------------------

        df["DATA"] = pd.to_datetime(
            df["DATA"],
            errors="coerce"
        )


        # ----------------------------------
        # HORA
        # ----------------------------------

        df["HORA"] = (
            df["HORA"]
            .astype("string")
            .str.strip()
        )


        # ----------------------------------
        # NÚMEROS
        # ----------------------------------

        for coluna in colunas_numericas:

            df[coluna] = (
                df[coluna]
                .astype("string")
                .str.strip()
                .str.replace(",", ".", regex=False)
            )

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )


        # ----------------------------------
        # NOME DO ARQUIVO DE SAÍDA
        # ----------------------------------

        nome_arquivo = arquivo_entrada.stem.replace(
            "_todas_causas_tipos",
            "_tratado"
        )

        arquivo_saida = (
            PASTA_TRATADOS /
            f"{nome_arquivo}.csv"
        )


        # ----------------------------------
        # SALVAR
        # ----------------------------------

        df.to_csv(
            arquivo_saida,
            sep=";",
            index=False,
            encoding="utf-8-sig"
        )


        # ----------------------------------
        # VALIDAÇÃO
        # ----------------------------------

        print("\nResultado:")

        print(
            f"Linhas finais: "
            f"{len(df):,}"
        )

        print(
            f"Colunas finais: "
            f"{len(df.columns)}"
        )

        print(
            f"Acidentes distintos: "
            f"{df['ID_ACIDENTE'].nunique():,}"
        )

        print(
            f"Valores vazios: "
            f"{df.isna().sum().sum():,}"
        )

        print(
            f"Arquivo criado: "
            f"{arquivo_saida}"
        )


    except Exception as erro:

        print("\nERRO AO PROCESSAR O ARQUIVO:")
        print(erro)


# ==========================================
# FINAL
# ==========================================

print("\n==========================================")
print("TRATAMENTO CONCLUÍDO")
print("==========================================")

arquivos_tratados = sorted(
    PASTA_TRATADOS.glob("acidentes*_tratado.csv")
)

print(
    f"Arquivos tratados encontrados: "
    f"{len(arquivos_tratados)}"
)

for arquivo in arquivos_tratados:
    print(f"- {arquivo.name}")

print("\nProcesso finalizado.")