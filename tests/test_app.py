import pytest

from app import app, reset_tickets


@pytest.fixture
def client():
    reset_tickets()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_returns_200(client):
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_ticket_1_has_a_title(client):
    response = client.get("/api/tickets/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Laptop not charging"


def test_unknown_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404


# Add your own tests below: one failing test for each bug you find,
# plus at least 5 negative tests.

def test_list_tickets_sorted_by_priority(client):
    response = client.get("/api/tickets")

    assert response.status_code == 200

    data = response.get_json()
    priorities = [ticket["priority"] for ticket in data]

    assert priorities == ["High", "High", "Medium", "Medium", "Low"]

def test_create_ticket_empty_title_returns_400(client):
    payload = {
        "title": "",
        "description": "Testing empty ticket title",
        "category": "Hardware",
        "priority": "High"
    }

    response = client.post("/api/tickets", json=payload)

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Title is required"