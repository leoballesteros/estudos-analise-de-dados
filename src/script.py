from __future__ import annotations

from pathlib import Path

import pandas as pd


def ler_xlsx_com_pandas(
    nome_arquivo: str | Path,
    sheet: str | int = 0,
    posicao_cabecalho: int | None = 0,
) -> pd.DataFrame:
    """
    Lê um arquivo .xlsx usando pandas e retorna um DataFrame.

    Parâmetros:
        nome_arquivo: Caminho/arquivo .xlsx (ex.: "quadro_janeiro.xlsx").
        sheet: Nome ou índice (0-based) da aba.
        posicao_cabecalho: Linha (0-based) do cabeçalho. Use None se o arquivo não tiver cabeçalho.

    Retorno:
        Um pandas.DataFrame com os dados lidos da planilha.
    """

    caminho = Path(nome_arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    if not isinstance(sheet, (str, int)):
        raise TypeError("O parâmetro 'sheet' precisa ser str (nome) ou int (índice).")

    if posicao_cabecalho is not None and posicao_cabecalho < 0:
        raise ValueError("O parâmetro 'posicao_cabecalho' precisa ser >= 0 ou None.")

    try:
        dataframe = pd.read_excel(
            caminho,
            sheet_name=sheet,
            header=posicao_cabecalho,
            engine="openpyxl",
        )
    except ImportError as exc:
        raise ImportError(
            "Dependências ausentes para ler .xlsx. Instale com: pip install pandas openpyxl"
        ) from exc

    return dataframe


def remover_linhas_totalmente_vazias(
    dataframe: pd.DataFrame,
    valores_vazios_adicionais: set[str] | None = None,
) -> pd.DataFrame:
    """
    Remove linhas em que TODAS as colunas estejam vazias.

    Considera como "vazio":
    - NaN/None (valores nulos do pandas)
    - strings vazias ("")
    - strings contendo apenas espaços em branco (ex.: "   ")
    - por padrão, também considera "-" (traço) como vazio (comum em planilhas como placeholder)

    Observações:
    - Retorna um NOVO DataFrame (não modifica o original).
    - Mantém o índice original (não dá reset_index).
    """

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("O parâmetro 'dataframe' precisa ser um pandas.DataFrame.")

    if dataframe.shape[1] == 0:
        return dataframe.iloc[0:0].copy()

    placeholders_vazios = {"", "-", "–", "—"}
    if valores_vazios_adicionais:
        placeholders_vazios |= {str(v) for v in valores_vazios_adicionais}

    celula_vazia = dataframe.isna()

    for coluna in dataframe.columns:
        serie = dataframe[coluna]
        if pd.api.types.is_object_dtype(serie) or pd.api.types.is_string_dtype(serie):
            serie_str = serie.astype("string")
            serie_strip = serie_str.str.strip()
            celula_vazia[coluna] = celula_vazia[coluna] | (
                serie_strip.isna()
                | (serie_strip == "")
                | serie_strip.isin(placeholders_vazios)
            )

    linhas_totalmente_vazias = celula_vazia.all(axis=1)
    return dataframe.loc[~linhas_totalmente_vazias].copy()


def gerar_xlsx_apenas_colunas(
    arquivo_origem: str | Path,
    arquivo_destino: str | Path,
    colunas_desejadas: list[str],
    sheet: str | int = 0,
    posicao_cabecalho: int | None = 0,
) -> pd.DataFrame:
    """
    Lê um .xlsx e gera um novo arquivo contendo apenas as colunas desejadas.

    - Retorna o DataFrame final (somente com as colunas).
    - Escreve o resultado em `arquivo_destino` (xlsx).
    - Faz correspondência de colunas ignorando maiúsculas/minúsculas e espaços extras.
    """

    if not colunas_desejadas:
        raise ValueError("A lista 'colunas_desejadas' não pode estar vazia.")

    df = ler_xlsx_com_pandas(
        nome_arquivo=arquivo_origem,
        sheet=sheet,
        posicao_cabecalho=posicao_cabecalho,
    )

    def normalizar_coluna(valor: object) -> str:
        texto = str(valor).replace("\u00a0", " ")
        return " ".join(texto.strip().upper().split())

    colunas_por_chave: dict[str, list[str]] = {}
    for col in df.columns:
        chave = normalizar_coluna(col)
        colunas_por_chave.setdefault(chave, []).append(str(col))

    faltando: list[str] = []
    selecionadas: list[str] = []
    for col in colunas_desejadas:
        chave = normalizar_coluna(col)
        candidatas = colunas_por_chave.get(chave)
        if not candidatas:
            faltando.append(col)
            continue
        if len(candidatas) > 1:
            raise KeyError(
                f"Coluna ambígua '{col}'. Candidatas encontradas no arquivo: {candidatas}"
            )
        selecionadas.append(candidatas[0])

    if faltando:
        disponiveis = list(df.columns)
        raise KeyError(
            "Colunas não encontradas no arquivo: "
            f"{faltando}. Colunas disponíveis: {disponiveis}"
        )

    df_final = df.loc[:, selecionadas].copy()

    caminho_destino = Path(arquivo_destino)
    df_final.to_excel(caminho_destino, index=False, engine="openpyxl")
    return df_final
