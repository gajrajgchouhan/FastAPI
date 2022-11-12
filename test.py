import requests


def test_create_task():
    r = requests.post("http://localhost:8000/v1/tasks", json={"title": "My First Task"})
    assert r.status_code == 201
    assert isinstance(r.json()["id"], int)
    assert len(r.json()) == 1


def test_list_all_tasks():
    r = requests.get("http://localhost:8000/v1/tasks")
    assert r.status_code == 200
    assert isinstance(r.json()["tasks"], list)
    assert len(r.json()) == 1
    assert isinstance(r.json()["tasks"][0]["id"], int)
    assert isinstance(r.json()["tasks"][0]["title"], str)
    assert isinstance(r.json()["tasks"][0]["is_completed"], bool)
    assert len(r.json()["tasks"][0]) == 3


def test_get_task():
    r = requests.get("http://localhost:8000/v1/tasks/1")
    print(r.json())
    assert r.status_code == 200
    assert isinstance(r.json(), dict)
    assert isinstance(r.json()["id"], int)
    assert isinstance(r.json()["title"], str)
    assert isinstance(r.json()["is_completed"], bool)
    assert len(r.json()) == 3


def test_get_wrong_task():
    r = requests.get("http://localhost:8000/v1/tasks/2")
    assert r.status_code == 404
    assert "error" in r.json()
    assert isinstance(r.json()["error"], str)
    assert r.json()["error"] == "There is no task at that id"


def test_update_task():
    r = requests.put("http://localhost:8000/v1/tasks/1", json={"title": "My 1st Task", "is_completed": True})
    assert r.status_code == 204
    assert not r.content


def test_delete_task():
    r = requests.delete("http://localhost:8000/v1/tasks/1")
    assert r.status_code == 204
    assert not r.content


def test_delete_task():
    r = requests.delete("http://localhost:8000/v1/tasks/2")
    assert r.status_code == 204
    assert not r.content


def test_create_bulk_task():
    js = {
        "tasks": [
            {"title": "Test Task 1", "is_completed": True},
            {"title": "Test Task 2", "is_completed": False},
            {"title": "Test Task 3", "is_completed": True},
        ]
    }
    r = requests.post("http://localhost:8000/v1/tasks", json=js)
    assert r.status_code == 201
    assert isinstance(r.json()["tasks"][0]["id"], int)
    assert isinstance(r.json()["tasks"][1]["id"], int)
    assert isinstance(r.json()["tasks"][2]["id"], int)
    assert len(r.json()["tasks"]) == 3


def test_delete_task():
    js = {"tasks": [{"id": 2}, {"id": 3}, {"id": 4}]}
    r = requests.delete("http://localhost:8000/v1/tasks", json=js)
    assert r.status_code == 204
    assert not r.content
