from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_sheets():
    response = client.get("/sheets/")
    assert response.status_code == 200
    assert response.json() == []
