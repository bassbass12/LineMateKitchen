from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "LineMate Kitchen API is running"}


def test_get_documents():
    response = client.get("/documents/")
    assert response.status_code == 200


def test_get_document_by_id():
    response = client.get("/documents/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Food Safety SOP"


def test_missing_document():
    response = client.get("/documents/999")
    assert response.status_code == 404


def test_get_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200


def test_get_ticket_by_id():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Broken grill"


def test_missing_ticket():
    response = client.get("/tickets/999")
    assert response.status_code == 404


def test_create_document():
    document = {
        "id": 100,
        "title": "Test Document",
        "category": "SOP",
        "body": "Test body",
        "owner_id": 10,
        "last_reviewed_at": "2026-09-20T10:00:00"
    }

    response = client.post("/documents/", json=document)

    assert response.status_code == 200
    assert response.json()["title"] == "Test Document"


def test_create_comment():
    comment = {
        "id": 100,
        "ticket_id": 1,
        "author_id": 10,
        "body": "Test comment",
        "created_at": "2026-09-28T20:00:00"
    }

    response = client.post("/comments/", json=comment)

    assert response.status_code == 200
    assert response.json()["body"] == "Test comment"


def test_get_comments():
    response = client.get("/comments/")
    assert response.status_code == 200


def test_ticket_analytics():
    response = client.get("/analytics/tickets")
    assert response.status_code == 200


def test_stale_documents():
    response = client.get("/analytics/stale-documents")
    assert response.status_code == 200


def test_ownership_mismatch():
    response = client.get("/analytics/ownership-mismatch")
    assert response.status_code == 200


def test_triage():
    response = client.get("/analytics/triage")
    assert response.status_code == 200