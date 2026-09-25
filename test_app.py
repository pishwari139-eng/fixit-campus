import pytest

from app import app, problems


@pytest.fixture
def client():
    app.config["TESTING"] = True

    problems.clear()

    with app.test_client() as client:
        yield client

    problems.clear()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_add_problem(client):
    response = client.post(
        "/add",
        data={
            "title": "Broken Fan",
            "category": "Maintenance",
            "location": "Classroom 101",
            "description": "The ceiling fan is not working.",
            "priority": "High"
        }
    )

    assert response.status_code == 302
    assert len(problems) == 1
    assert problems[0]["title"] == "Broken Fan"
    assert problems[0]["status"] == "Reported"


def test_invalid_problem(client):
    response = client.post(
        "/add",
        data={
            "title": "",
            "category": "Maintenance",
            "location": "Classroom 101",
            "description": "The fan is not working.",
            "priority": "High"
        }
    )

    assert response.status_code == 400
    assert len(problems) == 0
