"""Testes automatizados da API de Tarefas.

Usa o TestClient do FastAPI (simula requisições sem subir o servidor) com o
módulo unittest da biblioteca padrão.

Rodar a partir da raiz do repositório:

    python -m unittest discover -s api -p "test_*.py" -v
"""

import unittest

from fastapi.testclient import TestClient
from main import _reset, app


class TestAPITarefas(unittest.TestCase):
    def setUp(self):
        _reset()                       # estado limpo antes de cada teste
        self.client = TestClient(app)

    # ------------------------------------------------------------------
    def test_raiz_responde(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("mensagem", resp.json())

    def test_lista_comeca_vazia(self):
        resp = self.client.get("/tarefas")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    def test_criar_tarefa(self):
        resp = self.client.post("/tarefas", json={"titulo": "Estudar FastAPI"})
        self.assertEqual(resp.status_code, 201)
        corpo = resp.json()
        self.assertEqual(corpo["id"], 1)
        self.assertEqual(corpo["titulo"], "Estudar FastAPI")
        self.assertFalse(corpo["concluida"])

    def test_buscar_tarefa_existente(self):
        self.client.post("/tarefas", json={"titulo": "Tarefa 1"})
        resp = self.client.get("/tarefas/1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["titulo"], "Tarefa 1")

    def test_buscar_tarefa_inexistente_404(self):
        resp = self.client.get("/tarefas/999")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json()["detail"], "Tarefa não encontrada")

    def test_atualizar_tarefa(self):
        self.client.post("/tarefas", json={"titulo": "Antigo"})
        resp = self.client.put("/tarefas/1", json={"titulo": "Novo", "concluida": True})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["titulo"], "Novo")
        self.assertTrue(resp.json()["concluida"])

    def test_atualizar_inexistente_404(self):
        resp = self.client.put("/tarefas/999", json={"titulo": "X"})
        self.assertEqual(resp.status_code, 404)

    def test_remover_tarefa(self):
        self.client.post("/tarefas", json={"titulo": "Para remover"})
        resp = self.client.delete("/tarefas/1")
        self.assertEqual(resp.status_code, 204)
        # depois de remover, buscar deve dar 404
        self.assertEqual(self.client.get("/tarefas/1").status_code, 404)

    def test_remover_inexistente_404(self):
        self.assertEqual(self.client.delete("/tarefas/999").status_code, 404)

    def test_titulo_vazio_gera_422(self):
        # título com menos de 1 caractere é barrado pela validação do Pydantic
        resp = self.client.post("/tarefas", json={"titulo": ""})
        self.assertEqual(resp.status_code, 422)

    def test_campo_faltando_gera_422(self):
        resp = self.client.post("/tarefas", json={"concluida": True})
        self.assertEqual(resp.status_code, 422)

    def test_filtro_por_concluida(self):
        self.client.post("/tarefas", json={"titulo": "A", "concluida": True})
        self.client.post("/tarefas", json={"titulo": "B", "concluida": False})

        concluidas = self.client.get("/tarefas", params={"concluida": True}).json()
        self.assertEqual(len(concluidas), 1)
        self.assertEqual(concluidas[0]["titulo"], "A")


if __name__ == "__main__":
    unittest.main(verbosity=2)
