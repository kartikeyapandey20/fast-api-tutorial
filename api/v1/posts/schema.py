from pydantic import BaseModel
from datetime import datetime
from api.v1.user.schemas import UserOut
class PostSchema(BaseModel):
    title : str
    content : str 
    published : bool = True
    
class Post(PostSchema):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    class Config:
        orm_mode = True
        
class PostVote(PostSchema):
    id : int
    created_at : datetime
    owner_id : int
    votes : int
    class Config:
        orm_mode = True