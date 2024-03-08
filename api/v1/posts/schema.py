from pydantic import BaseModel

class PostSchema(BaseModel):
    title : str
    content : str
    published : bool = True