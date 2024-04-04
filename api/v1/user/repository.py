from api.v1.user.models import User
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException , status
from core.deps import get_db
from .schemas import UserSchema
from passlib.context import CryptContext
from core.security import hash_password
class UserRepository:
    def create_user(self, user : UserSchema ,db : Session = Depends(get_db)):
        
        #hash the password
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        
        new_user = User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    def get_user_by_id(self,id:int , db : Session = Depends(get_db)):
        user = db.query(User).filter(User.id == id ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"User not found"
            )
            
        return user