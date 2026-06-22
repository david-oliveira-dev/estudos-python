# Estudos em Python 🐍

[![CI](https://github.com/david-oliveira-dev/estudos-python/actions/workflows/ci.yml/badge.svg)](https://github.com/david-oliveira-dev/estudos-python/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Trilha de estudos de **Python do zero até APIs**, organizada em notebooks Jupyter.
Cada notebook tem explicação em texto + código executável, indo dos fundamentos
da linguagem até a construção de uma API real com **FastAPI**.

Faz parte da minha preparação para a faculdade de **Engenharia de Software**.

## Trilha de estudos

| # | Notebook | Tema |
|---|----------|------|
| 01 | `01_fundamentos.ipynb` | variáveis, tipos, operadores, entrada e saída |
| 02 | `02_controle_de_fluxo.ipynb` | `if/elif/else`, `while`, `for`, `range` |
| 03 | `03_estruturas_de_dados.ipynb` | listas, tuplas, dicionários e conjuntos |
| 04 | `04_funcoes.ipynb` | `def`, parâmetros, `*args/**kwargs`, `lambda`, escopo, type hints |
| 05 | `05_strings.ipynb` | métodos de string, fatiamento, f-strings, formatação |
| 06 | `06_erros_e_excecoes.ipynb` | `try/except/finally`, `raise`, exceções personalizadas |
| 07 | `07_orientacao_a_objetos.ipynb` | classes, objetos, herança, encapsulamento, dunder methods |
| 08 | `08_modulos_e_pacotes.ipynb` | `import`, módulos, pacotes, `pip`, ambientes virtuais |
| 09 | `09_arquivos_csv_json.ipynb` | ler/escrever arquivos texto, CSV e JSON |
| 10 | `10_pythonic.ipynb` | comprehensions, geradores, iteradores, `enumerate/zip` |
| 11 | `11_biblioteca_padrao.ipynb` | `datetime`, `math`, `random`, `collections`, `pathlib` |
| 12 | `12_testes_automatizados.ipynb` | `unittest`, asserts, organização de testes |
| 13 | `13_consumindo_apis.ipynb` | HTTP, status codes, JSON, biblioteca `requests` |
| 14 | `14_construindo_uma_api.ipynb` | criando uma API REST com **FastAPI** |

## Projeto capstone — API com FastAPI

A pasta [`api/`](api/) traz a aplicação final do estudo: uma API REST de tarefas
(_to-do_), com operações CRUD completas e **testes automatizados**.

```bash
# 1. criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

# 2. instalar as dependências
pip install -r requirements.txt

# 3. rodar a API (docs interativas em http://127.0.0.1:8000/docs)
uvicorn api.main:app --reload

# 4. rodar os testes da API
python -m unittest discover -s api -p "test_*.py" -v
```

## Como usar este repositório

- Os notebooks **01 a 12** usam apenas a **biblioteca padrão** do Python — não
  precisa instalar nada além do próprio Python para estudá-los.
- Os notebooks **13 e 14** usam `requests` e `fastapi` (veja `requirements.txt`).
- Recomendo seguir a ordem numérica: cada tema usa o anterior.

## Qualidade

- **Lint:** [ruff](https://docs.astral.sh/ruff/) (`ruff check .`)
- **Testes:** `unittest` (biblioteca padrão)
- **CI:** GitHub Actions roda lint + validação dos notebooks + testes da API em
  Python 3.11 e 3.12 a cada push.

## 📫 Contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/david-oliveira-9970a42a5)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/david-oliveira-dev)
