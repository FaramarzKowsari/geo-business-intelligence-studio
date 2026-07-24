from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_sample_search() -> None:
    response = client.post(
        "/api/search",
        json={
            "provider": "sample",
            "query": "coffee",
            "city": "Amsterdam",
            "radius_m": 5000,
            "limit": 20,
            "deduplicate": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["provider"] == "sample"
    assert data["businesses"]
    assert all(0 <= item["quality_score"] <= 100 for item in data["businesses"])


def test_google_provider_requires_key() -> None:
    response = client.post(
        "/api/search",
        json={
            "provider": "google_places",
            "query": "coffee",
            "city": "Amsterdam",
        },
    )
    assert response.status_code == 400
    assert "GOOGLE_PLACES_API_KEY" in response.json()["detail"]


def test_analysis_without_ai_key() -> None:
    search = client.post(
        "/api/search",
        json={"provider": "sample", "query": "coffee", "city": "Amsterdam"},
    ).json()
    response = client.post(
        "/api/analyze",
        json={"businesses": search["businesses"], "instruction": "Summarize the dataset."},
    )
    assert response.status_code == 200
    assert response.json()["provider"] == "deterministic"
