from typing import Optional
from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from api.v1 import api_router
from db.database import Base , engine
from api.v1.posts import models as PostModels
from api.v1.user import models as UserModels

app = FastAPI()
app.include_router(api_router)

UserModels.Base.metadata.create_all(bind=engine)
PostModels.Base.metadata.create_all(bind=engine)


# my_posts = [{"id" : 1,"title": "this is title","content": "this content"},{"id" : 2,"title": "this is title 2","content": "this content 2"} ]
# class Post(BaseModel):
#     title : str
#     content : str
#     publish  : bool  = True
#     rating : Optional[int] = None

# def find_index_post(id):
#     for i , p in enumerate(my_posts):
#         if my_posts[i].id == id:
#             return i
# @app.get("/")
# def root():
#     return {"message" : "hello world"}

# @app.get("/get_post")
# def get_post():
#     return  {"data" : [1,2,3,5]}

# @app.post("/createpost")
# def create_post(payload : dict = Body(...)):
#     return {"message": "Post Created"}

# @app.post("/post")
# def create_post(new_post : Post):
#     print("Title: ", new_post.title)
#     print("Content: ", new_post.content)
    
#     return {"message": new_post.dict()}


# @app.get("/posts")
# def get_post():
#     return  {"data" : my_posts}

# @app.post("/posts/create",status_code=status.HTTP_201_CREATED)
# def create_post(post : Post):
#     new_post = post.dict()
#     new_post["id"] = randrange(0,10000)
#     my_posts.append(new_post)
#     return {"message": my_posts}


# @app.get("/posts/{id}")
# def get_post_id(id : int , response : Response):
#     print(id)
#     if not id:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message" : "id is required"}
#     return {"data" : f"here is the post {id}"}

# @app.delete("/delete_post/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id : int):
#     index = find_index_post(id)
#     my_posts.pop(index)
#     return {"message" : "delete successful"}

# @app.put("/posts/{id}")
# def update_post(id : int, post : Post):
    # index = find_index_post(id)
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # return {"message" : post_dict}