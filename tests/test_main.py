from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_tasks():
    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task():
    response = client.get("/api/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_nonexistent_task():
    response = client.get("/api/tasks/999")

    assert response.status_code == 404


def test_create_task():
    response = client.post(
        "/api/tasks",
        json={
            "id": 100,
            "title": "Test task",
            "completed": False
        }
    )

    assert response.status_code == 201
    assert response.json()["id"] == 100


def test_update_task():
    response = client.put(
        "/api/tasks/100",
        json={
            "id": 100,
            "title": "Updated task",
            "completed": True
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated task"
    assert response.json()["completed"] is True


def test_delete_task():
    response = client.delete("/api/tasks/100")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"