
import pytest
from api.v1.vote.models import Voter

@pytest.fixture()
def test_vote(test_user, session ,test_post):
    new_vote = Voter(user_id=test_user["id"], post_id=test_post[3].id)
    session.add(new_vote)
    session.commit()

def test_votes_on_post(authorized_client, test_post):
    response = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 1})
    assert response.status_code == 201
    
def test_votes_on_post_twice(authorized_client, test_post,test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 1})
    assert response.status_code == 409
    
def test_delete_vote(authorized_client, test_post, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 0})
    assert response.status_code == 201
    
def test_delete_vote_non_exist(authorized_client, test_post):
    response = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 0})
    assert response.status_code == 404
    
def test_vote_post_non_exist(authorized_client, test_post):
    response = authorized_client.post("/vote/", json={"post_id": 8000, "dir": 1})
    assert response.status_code == 404
    
def test_vote_unauthorized_user(client, test_post):
    response = client.post("/vote/", json={"post_id": test_post[3].id, "dir": 1})
    assert response.status_code == 401