from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from script import (  # noqa: E402
    gerar_xlsx_apenas_colunas,
    ler_xlsx_com_pandas,
    remover_linhas_totalmente_vazias,
)




if __name__ == "__main__":
    # 1) Gera o arquivo limpo (remove linhas totalmente vazias)
    df = ler_xlsx_com_pandas(
        nome_arquivo=ROOT / "data" / "raw" / "quadro_janeiro.xlsx",
        sheet="Quadro Operacional",
        posicao_cabecalho=1,
    )
    df_limpo = remover_linhas_totalmente_vazias(df)
    arquivo_limpo = ROOT / "data" / "processed" / "quadro_janeiro_limpo.xlsx"
    df_limpo.to_excel(arquivo_limpo, index=False, engine="openpyxl")
    print("Arquivo 'quadro_janeiro_limpo.xlsx' criado com sucesso.")

    # 2) Gera um novo arquivo só com as colunas solicitadas
    colunas = [
        "CELULA",
        "MATRICULA22",
        "FUNCIONARIO",
        "NOME SOCIAL",
        "SUPERVISOR",
        "STATUS",
        "CARGA_HORARIA",
        "DT_DESLIGAMENTO",
        "FUNCAO",
        "GO LIVE COLABORADOR",
    ]
    gerar_xlsx_apenas_colunas(
        arquivo_origem=arquivo_limpo,
        arquivo_destino=ROOT / "outputs" / "reports" / "quadro_janeiro_apenas_colunas.xlsx",
        colunas_desejadas=colunas,
        sheet=0,
        posicao_cabecalho=0,
    )
    print("Arquivo 'quadro_janeiro_apenas_colunas.xlsx' criado com sucesso.")
