import pandas as pd
from pathlib import Path


# ==========================================
# CONFIGURAÇÕES
# ==========================================

PASTA_TRATADOS = Path("dados_tratados")


# ==========================================
# LOCALIZAR ARQUIVOS
# ==========================================

arquivos = sorted(
    PASTA_TRATADOS.glob("acidentes*_tratado.csv")
)

print("==========================================")
print("AUDITORIA GERAL - BASES DA PRF")
print("==========================================")

print(f"Arquivos encontrados: {len(arquivos)}")


if not arquivos:
    print("\nNenhum arquivo tratado encontrado.")
    raise SystemExit


# Lista para guardar o resumo de cada ano
resumo_anos = []


# ==========================================
# PROCESSAR CADA ANO
# ==========================================

for arquivo in arquivos:

    print("\n------------------------------------------")
    print(f"Auditando: {arquivo.name}")
    print("------------------------------------------")

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    # --------------------------------------
    # IDENTIFICAR O ANO
    # --------------------------------------

    df["DATA"] = pd.to_datetime(
        df["DATA"],
        errors="coerce"
    )

    ano = df["DATA"].dt.year.dropna().mode()

    if len(ano) > 0:
        ano = int(ano.iloc[0])
    else:
        ano = "NÃO IDENTIFICADO"


    # --------------------------------------
    # INFORMAÇÕES GERAIS
    # --------------------------------------

    linhas = len(df)
    colunas = len(df.columns)
    acidentes = df["ID_ACIDENTE"].nunique()

    valores_vazios = int(
        df.isna().sum().sum()
    )

    data_minima = df["DATA"].min()
    data_maxima = df["DATA"].max()

    datas_invalidas = int(
        df["DATA"].isna().sum()
    )


    # --------------------------------------
    # HORÁRIOS
    # --------------------------------------

    horarios_vazios = int(
        df["HORA"].isna().sum()
    )


    # --------------------------------------
    # KM
    # --------------------------------------

    km_vazios = int(
        df["KM"].isna().sum()
    )


    # --------------------------------------
    # GRAVIDADE
    # --------------------------------------

    gravidades = (
        df["GRAVIDADE"]
        .value_counts(dropna=False)
    )


    # --------------------------------------
    # ESTADOS
    # --------------------------------------

    estados = df["ESTADO"].nunique()


    # --------------------------------------
    # CAUSAS
    # --------------------------------------

    causas = df["CAUSA"].nunique()


    # --------------------------------------
    # CONDIÇÕES METEOROLÓGICAS
    # --------------------------------------

    condicoes_meteorologicas = (
        df["CONDICAO_METEOROLOGICA"]
        .nunique()
    )


    # --------------------------------------
    # VEÍCULOS
    # --------------------------------------

    veiculos = df["VEICULO"].nunique()


    # --------------------------------------
    # VÍTIMAS
    # --------------------------------------

    mortos = df["MORTOS"].sum()
    feridos_graves = df["FERIDOS_GRAVES"].sum()
    feridos_leves = df["FERIDOS_LEVES"].sum()
    ilesos = df["ILESOS"].sum()


    # --------------------------------------
    # EXIBIR RESULTADO
    # --------------------------------------

    print(f"Ano: {ano}")
    print(f"Linhas: {linhas:,}")
    print(f"Colunas: {colunas}")
    print(f"Acidentes distintos: {acidentes:,}")
    print(f"Valores vazios: {valores_vazios:,}")
    print(f"Data mínima: {data_minima}")
    print(f"Data máxima: {data_maxima}")
    print(f"Datas inválidas: {datas_invalidas:,}")
    print(f"Horários vazios: {horarios_vazios:,}")
    print(f"KM vazios: {km_vazios:,}")
    print(f"Estados: {estados}")
    print(f"Causas: {causas}")
    print(
        f"Condições meteorológicas: "
        f"{condicoes_meteorologicas}"
    )
    print(f"Tipos de veículos: {veiculos}")

    print("\nGravidade:")
    print(
        gravidades.to_string()
    )

    print("\nIndicadores de vítimas:")
    print(f"Ilesos: {ilesos:,.0f}")
    print(f"Feridos leves: {feridos_leves:,.0f}")
    print(f"Feridos graves: {feridos_graves:,.0f}")
    print(f"Mortos: {mortos:,.0f}")


    # --------------------------------------
    # GUARDAR RESUMO
    # --------------------------------------

    resumo_anos.append({
        "ANO": ano,
        "REGISTROS": linhas,
        "ACIDENTES_DISTINTOS": acidentes,
        "COLUNAS": colunas,
        "VALORES_VAZIOS": valores_vazios,
        "DATA_MINIMA": data_minima,
        "DATA_MAXIMA": data_maxima,
        "DATAS_INVALIDAS": datas_invalidas,
        "HORARIOS_VAZIOS": horarios_vazios,
        "KM_VAZIOS": km_vazios,
        "ESTADOS": estados,
        "CAUSAS": causas,
        "CONDICOES_METEOROLOGICAS": condicoes_meteorologicas,
        "VEICULOS": veiculos,
        "ILESO": ilesos,
        "FERIDOS_LEVES": feridos_leves,
        "FERIDOS_GRAVES": feridos_graves,
        "MORTOS": mortos
    })


# ==========================================
# TABELA FINAL DE RESUMO
# ==========================================

resumo = pd.DataFrame(
    resumo_anos
)

resumo = resumo.sort_values(
    by="ANO"
)


print("\n==========================================")
print("RESUMO GERAL DOS 7 ANOS")
print("==========================================")

print(
    resumo[
        [
            "ANO",
            "REGISTROS",
            "ACIDENTES_DISTINTOS",
            "VALORES_VAZIOS",
            "DATA_MINIMA",
            "DATA_MAXIMA",
            "DATAS_INVALIDAS",
            "HORARIOS_VAZIOS",
            "KM_VAZIOS",
            "MORTOS"
        ]
    ].to_string(index=False)
)


# ==========================================
# SOMATÓRIOS
# ==========================================

print("\n==========================================")
print("TOTAIS DO PERÍODO")
print("==========================================")

print(
    f"Total de registros: "
    f"{resumo['REGISTROS'].sum():,}"
)

print(
    f"Total de acidentes distintos: "
    f"{resumo['ACIDENTES_DISTINTOS'].sum():,}"
)

print(
    f"Total de ilesos: "
    f"{resumo['ILESO'].sum():,.0f}"
)

print(
    f"Total de feridos leves: "
    f"{resumo['FERIDOS_LEVES'].sum():,.0f}"
)

print(
    f"Total de feridos graves: "
    f"{resumo['FERIDOS_GRAVES'].sum():,.0f}"
)

print(
    f"Total de mortos: "
    f"{resumo['MORTOS'].sum():,.0f}"
)


# ==========================================
# VERIFICAÇÕES
# ==========================================

print("\n==========================================")
print("VERIFICAÇÕES")
print("==========================================")


if len(arquivos) == 7:
    print("✓ Os 7 arquivos tratados estão presentes.")
else:
    print(
        f"⚠ Foram encontrados apenas "
        f"{len(arquivos)} arquivos."
    )


if all(resumo["COLUNAS"] == 17):
    print("✓ Todos os arquivos possuem 17 colunas.")
else:
    print("⚠ Existe arquivo com quantidade diferente de colunas.")


if resumo["DATAS_INVALIDAS"].sum() == 0:
    print("✓ Não existem datas inválidas.")
else:
    print("⚠ Existem datas inválidas.")


if resumo["HORARIOS_VAZIOS"].sum() == 0:
    print("✓ Não existem horários vazios.")
else:
    print("⚠ Existem horários vazios.")


print("\n==========================================")
print("AUDITORIA GERAL CONCLUÍDA")
print("==========================================")