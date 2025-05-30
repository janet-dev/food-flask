import pytest
from app import app, db, Review

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_review(client):
    data = {
        "food_name": "Pizza",
        "reviewer_name": "Alice",
        "rating": 5,
        "comment": "Delicious!"
    }
    response = client.post("/api/reviews", json=data)
    assert response.status_code == 201
    resp_data = response.get_json()
    assert resp_data["food_name"] == "Pizza"
    assert resp_data["rating"] == 5

def test_get_reviews_empty(client):
    response = client.get("/api/reviews")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_review_not_found(client):
    response = client.get("/api/reviews/1")
    assert response.status_code == 404

def test_full_crud(client):
    # Create
    data = {
        "food_name": "Burger",
        "reviewer_name": "Bob",
        "rating": 4,
        "comment": "Tasty"
    }
    response = client.post("/api/reviews", json=data)
    assert response.status_code == 201
    review_id = response.get_json()["id"]

    # Read
    response = client.get(f"/api/reviews/{review_id}")
    assert response.status_code == 200
    assert response.get_json()["food_name"] == "Burger"

    # Update
    update_data = {"rating": 3}
    response = client.put(f"/api/reviews/{review_id}", json=update_data)
    assert response.status_code == 200
    assert response.get_json()["rating"] == 3

    # Delete
    response = client.delete(f"/api/reviews/{review_id}")
    assert response.status_code == 200

    # Confirm deleted
    response = client.get(f"/api/reviews/{review_id}")
    assert response.status_code == 404
