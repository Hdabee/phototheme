from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["mode"] in {"local-mock", "local-web-mock"}


def test_recommend_layout():
    response = client.post("/api/v1/recommend-layout", json={
        "photo_count": 4,
        "target_format": "square",
        "occasion": "general",
    })
    assert response.status_code == 200
    layouts = response.json()["recommended_layouts"]
    assert layouts
    assert layouts[0]["photo_count"] == 4
