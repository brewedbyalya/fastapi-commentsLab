import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.user import UserModel
from models.tea import TeaModel
from tests.lib import login
from main import app

def test_get_teas(test_app: TestClient, override_get_db):
    response = test_app.get("/api/teas")
    assert response.status_code == 200
    teas = response.json()
    assert isinstance(teas, list)
    assert len(teas) >= 2
    for tea in teas:
        assert 'id' in tea
        assert 'name' in tea
        assert 'in_stock' in tea
        assert 'rating' in tea
        assert 'user' in tea
        assert 'email' in tea['user']
        assert 'username' in tea['user']


def test_create_tea(test_app: TestClient, test_db: Session):

    user = UserModel(username='testUser123', email='hello@example.com')
    user.set_password('mys3cretp2ssw0rd')
    test_db.add(user)
    test_db.commit()

    headers = login(test_app, 'testUser123', 'mys3cretp2ssw0rd')
    tea_data = {
        "name": "Test Tea",
        "in_stock": True,
        "rating": 4
    }

    response = test_app.post("/api/teas", headers=headers, json=tea_data)

    assert response.status_code == 200
    assert response.json()["name"] == tea_data["name"]
    assert response.json()["in_stock"] == tea_data["in_stock"]
    assert response.json()["rating"] == tea_data["rating"]
    assert "id" in response.json()
    assert "user" in response.json()
    assert response.json()['user']["username"] == 'testUser123'

    tea_id = response.json()["id"]
    tea = test_db.query(TeaModel).filter(TeaModel.id == tea_id).first()
    assert tea is not None
    assert tea.name == tea_data["name"]
    assert tea.in_stock == tea_data["in_stock"]
    assert tea.rating == tea_data["rating"]
