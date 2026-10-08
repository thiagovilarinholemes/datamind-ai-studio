"""
Testes básicos dos endpoints da API.
"""

from fastapi.testclient import TestClient

from app.main import app


# Cliente de testes para simular requisições HTTP.
client = TestClient(app)


def test_root_returns_welcome_message():
    """
    Verifica se a rota raiz retorna a mensagem esperada.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert (
        "DataMind AI Studio"
        in response.json()["message"]
    )


def test_health_endpoint():
    """
    Verifica se o health check retorna status OK.
    """

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"