# Documentação: `ler_xlsx_com_pandas` (script.py)

## Objetivo

A função `ler_xlsx_com_pandas` lê um arquivo Excel `.xlsx` usando `pandas` e retorna um `DataFrame` com os dados da aba informada, respeitando a linha em que está o cabeçalho.

Arquivo alvo (exemplo do projeto): `quadro_janeiro.xlsx`.

---

## Assinatura

```py
def ler_xlsx_com_pandas(
    nome_arquivo: str | Path,
    sheet: str | int = 0,
    posicao_cabecalho: int | None = 0,
) -> pd.DataFrame:
```

---

## Parâmetros

### `nome_arquivo`
- Tipo: `str | Path`
- O que é: o caminho do arquivo `.xlsx` (pode ser relativo ao diretório do projeto).
- Exemplo: `"quadro_janeiro.xlsx"`

### `sheet`
- Tipo: `str | int`
- O que é:
  - `str`: nome da aba (por exemplo `"Janeiro"`).
  - `int`: índice da aba (0-based: `0` é a primeira aba).
- Padrão: `0`

### `posicao_cabecalho`
- Tipo: `int | None`
- O que é:
  - `int`: número da linha (0-based) que contém os nomes das colunas.
  - `None`: indica que **não existe cabeçalho**; nesse caso, o pandas cria colunas numéricas (0, 1, 2, ...).
- Padrão: `0`

Observação importante: “0-based” significa que a primeira linha do arquivo é `0`, a segunda é `1`, etc.

---

## Retorno

- Tipo: `pandas.DataFrame`
- O que contém: os dados lidos do Excel já organizados em formato tabular.

---

## Função extra: remover linhas totalmente vazias

O projeto também possui a função `remover_linhas_totalmente_vazias`, que remove linhas onde **todas** as colunas estão vazias.

Valores considerados vazios:
- `NaN` / `None`
- `""` (string vazia)
- `"   "` (apenas espaços)
- `"-"` (traço, comum como placeholder em planilhas)

Exemplo:
```py
from script import ler_xlsx_com_pandas, remover_linhas_totalmente_vazias

df = ler_xlsx_com_pandas("quadro_janeiro.xlsx", sheet="Quadro Operacional", posicao_cabecalho=1)
df_limpo = remover_linhas_totalmente_vazias(df)
```

---

## Exemplo de uso (projeto)

O arquivo `main.py` já contém um exemplo que lê o `quadro_janeiro.xlsx` e imprime as primeiras linhas:

```py
from script import ler_xlsx_com_pandas

df = ler_xlsx_com_pandas(
    nome_arquivo="quadro_janeiro.xlsx",
    sheet="Quadro Operacional",
    posicao_cabecalho=1,
)
print(df.head())
```

Observação sobre o arquivo `quadro_janeiro.xlsx`: a primeira aba é `instruções` (não é a base operacional). A base está na aba `Quadro Operacional` e o cabeçalho fica na linha `1` (0-based) dessa aba.

---

## Explicando a implementação (linha a linha, por blocos)

### 1) `Path(nome_arquivo)`
Código:
```py
caminho = Path(nome_arquivo)
```
Método/classe usada: `pathlib.Path`
- Por que usar:
  - Padroniza o caminho do arquivo.
  - Funciona bem com caminhos relativos/absolutos.
  - Integra diretamente com várias APIs do Python.

### 2) `caminho.exists()`
Código:
```py
if not caminho.exists():
    raise FileNotFoundError(...)
```
Método usado: `Path.exists()`
- O que faz: verifica se o arquivo realmente existe no disco antes de tentar ler.
- Benefício: falha mais cedo e com mensagem clara, em vez de estourar um erro genérico mais tarde.

### 3) Validação de tipos (`isinstance`)
Código:
```py
if not isinstance(sheet, (str, int)):
    raise TypeError(...)
```
Método/função usada: `isinstance(obj, tipos)`
- O que faz: garante que `sheet` seja `str` (nome da aba) ou `int` (índice).
- Benefício: evita que o `pandas.read_excel` retorne um tipo diferente (por exemplo, `dict` quando você passa uma lista de abas) ou erros difíceis de interpretar.

### 4) Validação do cabeçalho
Código:
```py
if posicao_cabecalho is not None and posicao_cabecalho < 0:
    raise ValueError(...)
```
- O que faz: impede valores inválidos (linhas negativas).
- `None` é permitido para indicar “sem cabeçalho”.

### 5) `pd.read_excel(...)`
Código:
```py
dataframe = pd.read_excel(
    caminho,
    sheet_name=sheet,
    header=posicao_cabecalho,
    engine="openpyxl",
)
```
Método usado: `pandas.read_excel`
- O que faz: lê a planilha do Excel e cria um `DataFrame`.

Parâmetros usados:
- `caminho`: o arquivo a ser lido.
- `sheet_name=sheet`:
  - controla qual aba será lida.
  - aceita `str` (nome) ou `int` (índice).
- `header=posicao_cabecalho`:
  - indica ao pandas em qual linha estão os nomes das colunas.
  - `0` significa “a primeira linha do arquivo é o cabeçalho”.
  - `None` significa “não existe cabeçalho”.
- `engine="openpyxl"`:
  - define explicitamente o motor de leitura para `.xlsx`.
  - evita ambiguidades dependendo da versão/ambiente.

### 6) Tratamento de dependências (`try/except ImportError`)
Código:
```py
try:
    ...
except ImportError as exc:
    raise ImportError("... pip install pandas openpyxl") from exc
```
- O que faz: se o ambiente não tiver `pandas` e/ou `openpyxl`, a função emite um erro mais orientativo.
- `from exc`: preserva o erro original como causa, ajudando no diagnóstico.

### 7) `return dataframe`
- Retorna o `DataFrame` final para o chamador.
- Isso permite que outras partes do projeto filtrem/limpem/transformem os dados depois (se necessário).

---

## Requisitos (dependências)

Para ler `.xlsx` via pandas, normalmente você precisa de:
- `pandas`
- `openpyxl`

Instalação típica:
```bash
pip install pandas openpyxl
```
