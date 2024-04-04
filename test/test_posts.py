from api.v1.posts.schema import PostVote ,Post

def test_get_all_posts(authorized_client,test_post):
    response = authorized_client.get("/posts/")
    
    def validate(post):
        return PostVote(**post)
    
    post_map = map(validate, response.json())
    
    post_list = list(post_map)
    
    assert len(response.json()) == len(test_post)
    assert response.status_code == 200

def  test_unauthorized_user_get_all_posts(client, test_post):
    response = client.get("/posts/")
    assert response.status_code == 401

def  test_unauthorized_user_get_one_posts(client, test_post):
    response = client.get(f"/posts/{test_post[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_post):
    response = authorized_client.get("/posts/88888")
    assert response.status_code == 404
    
def test_get_one_post(authorized_client, test_post):
    response = authorized_client.get(f"/posts/{test_post[0].id}")
    post = PostVote(**response.json())
    assert post.id == test_post[0].id
    assert post.title == test_post[0].title
    assert post.content == test_post[0].content
    
def test_create_post(authorized_client, test_user, test_post):
    response = authorized_client.post("/posts/", json={"title": "title", "content": "content"})
    created_post = Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.owner_id == test_user["id"]
    

def test_unauthorized_user_create_post(client, test_user, test_post):
    response = client.post("/posts/", json={"title": "title", "content": "content"})
    assert response.status_code == 401    
    
def test_unauthorized_user_delete_post(client, test_user, test_post):
    response = client.delete(f"/posts/{test_post[0].id}")
    assert response.status_code == 401
    
def test_delete_post(authorized_client, test_user, test_post):
    response = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert response.status_code == 204
    
def test_delete_post_not_exist(authorized_client, test_user, test_post):
    response = authorized_client.delete(f"/posts/88888")
    assert response.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_user, test_post):
    response = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert response.status_code == 403
    
def test_update_post(authorized_client, test_user, test_post):
    data = {"title": "updated title", "content": "updated content", "id": test_post[0].id}
    
    response = authorized_client.put(f"/posts/{test_post[0].id}", json=data)
    
    updated_post = Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == "updated title"
    assert updated_post.content == "updated content"
    assert updated_post.owner_id == test_user["id"]
    
def test_update_other_user_post(authorized_client, test_user, test_post):
    data = {"title": "updated title", "content": "updated content", "id": test_post[3].id}

    response = authorized_client.put(f"/posts/{test_post[3].id}", json=data)

    assert response.status_code == 403
    
    
def test_update_other_user_post(authorized_client, test_user, test_post):
    data = {"title": "updated title", "content": "updated content", "id": test_post[3].id}

    response = authorized_client.put(f"/posts/{test_post[3].id}", json=data)

    assert response.status_code == 403
    
def test_unauthorized_user_update_post(client, test_user, test_post):
    data = {"title": "updated title", "content": "updated content", "id": test_post[0].id}

    response = client.put(f"/posts/{test_post[0].id}", json=data)

    assert response.status_code == 401
    
def test_update_post_not_exist(authorized_client, test_user, test_post):
    data = {"title": "updated title", "content": "updated content", "id": test_post[0].id}

    response = authorized_client.put(f"/posts/88888", json=data)

    assert response.status_code == 404