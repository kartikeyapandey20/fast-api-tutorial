from api.v1.user.schemas import UserOut
import pytest
from api.v1.auth.schema import TokenResponse
from jose import jwt
from core.config import settings

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
def test_create_user(client):
    response = client.post("/user/", json={"email": "youmai1@example.com","password": "#VIP2888"})

    new_user = UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "youmai1@example.com"
    # assert response.json() == {"name": "John Doe"}
    
def test_login_user(client , test_user):
    response = client.post("/login/", data={"username": test_user["email"], "password": test_user["password"]})
    login_reponse  = TokenResponse(**response.json())
    payload = jwt.decode(login_reponse.access_token,settings.SECRET_KEY,settings.ALGORITHM)
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_reponse.token_type == "bearer"
    assert response.status_code == 200
    
def test_incorrect_login(client, test_user):
    response = client.post("/login/", data={"username": test_user["email"], "password": "XXXXXXXXX_password"})
    print(response.json())
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid username or password"}