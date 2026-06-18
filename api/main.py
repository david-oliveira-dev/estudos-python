"""API de Tarefas — projeto capstone da trilha de estudos.

Uma API REST completa (CRUD) construída com FastAPI, juntando tudo o que foi
estudado nos notebooks: funções, type hints, dicionários, validação e testes.

Como rodar (a partir da raiz do repositório, com o ambiente virtual ativo):

    pip install -r requirements.txt
    uvicorn api.main:app --reload

Depois abra a documentação interativa em http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Tarefas",
    description="CRUD de tarefas (to-do) — capstone do repositório estudos-python.",
    version="1.0.0",
)


# ----------------------------------------------------------------------
# Modelos (Pydantic valida os dados automaticamente)
# ----------------------------------------------------------------------
class TarefaEntrada(BaseModel):
    """Dados que o cliente envia ao criar ou atualizar uma tarefa."""

    titulo: str = Field(min_length=1, description="Descrição da tarefa.")
    concluida: bool = False


class Tarefa(TarefaEntrada):
    """Tarefa completa, já com o id gerado pela API."""

    id: int


# ----------------------------------------------------------------------
# "Banco de dados" em memória (simples, só para o estudo)
# ----------------------------------------------------------------------
_tarefas: dict[int, Tarefa] = {}
_proximo_id = 1


def _reset() -> None:
    """Limpa o estado. Usado pelos testes para começar sempre do zero."""
    global _tarefas, _proximo_id
    _tarefas = {}
    _proximo_id = 1


# ----------------------------------------------------------------------
# Rotas
# ----------------------------------------------------------------------
@app.get("/")
def raiz() -> dict:
    return {"mensagem": "API de Tarefas no ar!", "documentacao": "/docs"}


@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas(concluida: bool | None = None) -> list[Tarefa]:
    """Lista todas as tarefas. Filtro opcional: ?concluida=true|false."""
    tarefas = list(_tarefas.values())
    if concluida is not None:
        tarefas = [t for t in tarefas if t.concluida == concluida]
    return tarefas


@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def buscar_tarefa(tarefa_id: int) -> Tarefa:
    tarefa = _tarefas.get(tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@app.post("/tarefas", response_model=Tarefa, status_code=201)
def criar_tarefa(dados: TarefaEntrada) -> Tarefa:
    global _proximo_id
    tarefa = Tarefa(id=_proximo_id, **dados.model_dump())
    _tarefas[_proximo_id] = tarefa
    _proximo_id += 1
    return tarefa


@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, dados: TarefaEntrada) -> Tarefa:
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa = Tarefa(id=tarefa_id, **dados.model_dump())
    _tarefas[tarefa_id] = tarefa
    return tarefa


@app.delete("/tarefas/{tarefa_id}", status_code=204)
def remover_tarefa(tarefa_id: int) -> None:
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    del _tarefas[tarefa_id]
