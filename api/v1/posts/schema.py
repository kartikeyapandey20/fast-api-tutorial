from pydantic import BaseModel
from datetime import datetime
class PostSchema(BaseModel):
    title : str
    content : str 
    published : bool = True
    
class Post(PostSchema):
    id : int
    created_at : datetime
    class Config:
        orm_mode = True