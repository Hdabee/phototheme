from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "PhotoTheme" in response.text


def test_upload_validation_requires_files():
    response = client.post("/web/upload")
    assert response.status_code == 422
