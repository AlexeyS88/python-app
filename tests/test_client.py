from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from app.main import app

def test_get_tasks():
    with TestClient(app=app) as client:
        response = client.get("/tasks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_create_and_get_task(monkeypatch):
    monkeypatch.setattr("app.api.routers.task.publish_json", AsyncMock())
    with TestClient(app=app) as client:
        payload = {"title": "CI test task"}
        create_resp = client.post("/tasks", json=payload)
        assert create_resp.status_code in (200, 201)

        task_id = create_resp.json().get("id")
        assert task_id is not None

        patch_resp = client.patch(f"/tasks/{task_id}", json={"title": "Updated CI tasls"})
        assert patch_resp.status_code == 200

        client.delete(f"/tasks/{task_id}")

def test_task_not_found():
    with TestClient(app=app) as client:
        response = client.delete("/tasks/not-existent-id-1")
        assert response.status_code == 404