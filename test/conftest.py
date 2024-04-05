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

# Construct the SQLAlchemy database URL for testing
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker for testing
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Fixture to set up a new database session for each test
@pytest.fixture()
def session():
    # Drop and recreate all tables in the test database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Create a new session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture to provide a test client for endpoint testing
@pytest.fixture()
def client(session):
    # Override the get_db dependency to use the testing session
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# Fixture to create a test user for testing authentication
@pytest.fixture
def test_user(client):
    # Create a test user using the client
    user_data = {"email": "youmai1@example.com", "password": "#VIP2888"}
    response = client.post("/user/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

# Fixture to create a second test user for testing ownership
@pytest.fixture
def test_user_two(client):
    # Create another test user using the client
    user_data = {"email": "youmai2@example.com", "password": "#VIP2888"}
    response = client.post("/user/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

# Fixture to generate a JWT token for authorization
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" : test_user["id"]})

# Fixture to provide an authorized client with the JWT token
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

# Fixture to create test posts for endpoint testing
@pytest.fixture
def test_post(test_user, session, test_user_two):
    # Define sample post data
    post_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user["id"]},
        {"title": "second title", "content": "second content", "owner_id": test_user["id"]},
        {"title": "third title", "content": "third content", "owner_id": test_user["id"]},
        {"title": "fourth title", "content": "fourth content", "owner_id": test_user_two["id"]}
    ]
    
    # Function to create Post models from post data
    def create_post_model(post):
        return Post(**post)
    
    # Map the create_post_model function to create Post instances
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    
    # Add posts to the session and commit changes
    session.add_all(posts)
    session.commit()
    
    # Retrieve all posts from the session
    posts = session.query(Post).all()
    
    return posts
