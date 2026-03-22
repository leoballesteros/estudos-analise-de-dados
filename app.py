import pandas as pd


def corrigir_dados():
    df = pd.read_csv("dados.csv")

    colunas = ["empresa_origem", "cliente_destino"]
    for col in colunas:
        df[col] = df[col].fillna("")
        vazios = df[col].astype(str).str.strip() == ""
        df.loc[vazios, col] = "-"

    df.to_csv("dados.csv", index=False)


def gerar_origens_unicas(arquivo_entrada="dados.csv", arquivo_saida="origens_unicas.csv"):
    df = pd.read_csv(arquivo_entrada, usecols=["empresa_origem", "cnpj_origem"], dtype=str)
    df["empresa_origem"] = df["empresa_origem"].fillna("").str.strip()
    df["cnpj_origem"] = df["cnpj_origem"].fillna("").str.strip()

    df_unico = df.drop_duplicates(subset=["cnpj_origem"])

    if arquivo_saida:
        df_unico.to_csv(arquivo_saida, index=False)

    return df_unico


def preencher_empresa_origem_pelo_cnpj(
    arquivo_dados="dados.csv", arquivo_origens="origens_unicas.csv"
):
    df_dados = pd.read_csv(arquivo_dados, dtype=str)
    df_origens = pd.read_csv(arquivo_origens, dtype=str)

    df_origens_validas = df_origens[df_origens["empresa_origem"] != "-"].drop_duplicates(
        subset=["cnpj_origem"]
    )
    mapa = dict(zip(df_origens_validas["cnpj_origem"], df_origens_validas["empresa_origem"]))

    faltando_empresa = df_dados["empresa_origem"] == "-"
    substituicao = df_dados.loc[faltando_empresa, "cnpj_origem"].map(mapa)
    df_dados.loc[faltando_empresa & substituicao.notna(), "empresa_origem"] = substituicao

    df_dados.to_csv(arquivo_dados, index=False)
    return df_dados


if __name__ == "__main__":
    corrigir_dados()
    gerar_origens_unicas()
    preencher_empresa_origem_pelo_cnpj()