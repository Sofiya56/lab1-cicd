from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create(title="Test task", completed=False):
    r = client.post("/api/tasks", json={"title": title, "completed": completed})
    assert r.status_code == 201
    return r.json()


def test_get_tasks():
    r = client.get("/api/tasks")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_task():
    r = client.post("/api/tasks", json={"title": "Test", "completed": False})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test"
    assert data["id"] is not None


def test_get_task():
    t = create("Get me")
    r = client.get(f"/api/tasks/{t['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "Get me"


def test_get_nonexistent_task():
    assert client.get("/api/tasks/999999").status_code == 404


def test_update_task():
    t = create("Old")
    r = client.put(f"/api/tasks/{t['id']}", json={"title": "New", "completed": True})
    assert r.status_code == 200
    assert r.json()["title"] == "New"
    assert r.json()["completed"] is True


def test_delete_task():
    t = create("Delete me")
    assert client.delete(f"/api/tasks/{t['id']}").status_code == 204
    assert client.get(f"/api/tasks/{t['id']}").status_code == 404
