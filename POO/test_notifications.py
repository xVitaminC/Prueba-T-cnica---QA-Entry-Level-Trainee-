"""
Pruebas automatizadas para la Notification API
Casos cubiertos: TC01, TC02, TC03, TC04, TC09, TC10, TC11, TC12
Requisitos: pip install pytest httpx fastapi
"""

import pytest
from fastapi.testclient import TestClient
from main import app, history

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_historial():
    """Limpia el historial antes de cada prueba para evitar contaminación."""
    history._records.clear()
    yield
    history._records.clear()


# ─── POST /notifications ──────────────────────────────────────────────────────

class TestPostNotifications:

    def test_TC01_envio_valido_email(self):
        """TC01 - Envío válido por canal email debe retornar 201 y status sent."""
        response = client.post("/notifications", json={
            "userId": "123",
            "message": "Hola",
            "channel": "email"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["record"]["status"] == "sent"
        assert data["record"]["channel"] == "email"
        assert data["record"]["userId"] == "123"

    def test_TC02_envio_valido_sms(self):
        """TC02 - Envío válido por canal sms debe retornar 201 y status sent."""
        response = client.post("/notifications", json={
            "userId": "456",
            "message": "Mensaje SMS",
            "channel": "sms"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["record"]["status"] == "sent"
        assert data["record"]["channel"] == "sms"

    def test_TC03_canal_invalido(self):
        """TC03 - Canal no permitido debe retornar 422."""
        response = client.post("/notifications", json={
            "userId": "123",
            "message": "Hola",
            "channel": "push"
        })
        assert response.status_code == 422

    def test_TC04_falta_userId(self):
        """TC04 - Sin userId debe retornar 422."""
        response = client.post("/notifications", json={
            "message": "Hola",
            "channel": "email"
        })
        assert response.status_code == 422

    def test_TC05_falta_message(self):
        """TC05 - Sin message debe retornar 422."""
        response = client.post("/notifications", json={
            "userId": "123",
            "channel": "email"
        })
        assert response.status_code == 422

    def test_TC06_falta_channel(self):
        """TC06 - Sin channel debe retornar 422."""
        response = client.post("/notifications", json={
            "userId": "123",
            "message": "Hola"
        })
        assert response.status_code == 422

    def test_TC07_body_vacio(self):
        """TC07 - Body vacío debe retornar 422."""
        response = client.post("/notifications", json={})
        assert response.status_code == 422

    def test_TC08_userId_vacio(self):
        """TC08 - userId vacío debe retornar 422."""
        response = client.post("/notifications", json={
            "userId": "   ",
            "message": "Hola",
            "channel": "email"
        })
        assert response.status_code == 422


# ─── GET /notifications ───────────────────────────────────────────────────────

class TestGetNotifications:

    def test_TC09_historial_vacio(self):
        """TC09 - Sin envíos previos debe retornar data como lista vacía."""
        response = client.get("/notifications")
        assert response.status_code == 200
        assert response.json() == {"data": []}

    def test_TC10_historial_con_registros(self):
        """TC10 - Tras un POST exitoso, GET debe incluir la notificación enviada."""
        client.post("/notifications", json={
            "userId": "789",
            "message": "Test mensaje",
            "channel": "sms"
        })
        response = client.get("/notifications")
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["userId"] == "789"
        assert data[0]["message"] == "Test mensaje"
        assert data[0]["channel"] == "sms"

    def test_TC11_estructura_respuesta(self):
        """TC11 - La respuesta debe tener la clave 'data' como lista."""
        response = client.get("/notifications")
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert isinstance(body["data"], list)

    def test_TC12_campos_del_registro(self):
        """TC12 - Cada registro debe tener userId, message, channel, status, timestamp."""
        client.post("/notifications", json={
            "userId": "111",
            "message": "Verificar campos",
            "channel": "email"
        })
        response = client.get("/notifications")
        record = response.json()["data"][0]
        for campo in ["userId", "message", "channel", "status", "timestamp"]:
            assert campo in record, f"Falta el campo: {campo}"
