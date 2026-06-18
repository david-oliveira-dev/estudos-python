"""Valida todos os notebooks da pasta notebooks/.

Faz duas verificações, usando apenas a biblioteca padrão:

1. Cada arquivo .ipynb é um JSON válido e tem a estrutura mínima de notebook.
2. O código Python de cada célula compila (sintaxe correta) — não executa,
   apenas garante que não há erro de sintaxe.

Rodar:  python scripts/validar_notebooks.py
"""

import json
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "notebooks"


def validar_notebook(caminho: Path) -> list[str]:
    erros: list[str] = []
    try:
        nb = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"JSON inválido: {e}"]

    if "cells" not in nb:
        erros.append("não tem a chave 'cells'")
        return erros

    for i, celula in enumerate(nb["cells"]):
        if celula.get("cell_type") != "code":
            continue
        codigo = "".join(celula.get("source", []))
        try:
            compile(codigo, f"{caminho.name}[célula {i}]", "exec")
        except SyntaxError as e:
            erros.append(f"erro de sintaxe na célula {i}: {e}")
    return erros


def main() -> int:
    notebooks = sorted(PASTA.glob("*.ipynb"))
    if not notebooks:
        print("Nenhum notebook encontrado.")
        return 1

    total_erros = 0
    for nb in notebooks:
        erros = validar_notebook(nb)
        if erros:
            total_erros += len(erros)
            print(f"FALHOU  {nb.name}")
            for erro in erros:
                print(f"        - {erro}")
        else:
            print(f"OK      {nb.name}")

    print("-" * 50)
    if total_erros:
        print(f"{total_erros} problema(s) encontrado(s).")
        return 1
    print(f"Todos os {len(notebooks)} notebooks são válidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
