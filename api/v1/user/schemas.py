from pydantic import BaseModel , EmailStr
from datetime import datetime

class UserSchema(BaseModel):
    email : EmailStr
    password : str


class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True