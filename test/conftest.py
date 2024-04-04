from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import app

from core.config import settings
from core.deps import get_db
from db.database import Base
from alembic import command
from api.v1.auth.oauth2 import create_access_token
from api.v1.posts.models import Post
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {"email": "youmai1@example.com", "password": "#VIP2888"}

    response = client.post("/user/", json=user_data)
    
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user_two(client):
    user_data = {"email": "youmai2@example.com", "password": "#VIP2888"}

    response = client.post("/user/", json=user_data)
    
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" :test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(test_user,session,test_user_two):
    #generate me list of sample data for testing post
    post_data = [
        {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"]
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"]
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user_two["id"]
        }]
    
    def create_post_model(post):
        return Post(**post)
    
    post_map = map(create_post_model, post_data)

    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    posts = session.query(Post).all()
    
    return posts