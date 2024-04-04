from jose import JWTError , jwt
from datetime import datetime , timedelta
from .schema import TokenData
from fastapi import Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.deps import get_db
from api.v1.user.models import User
from core.config import settings
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data : dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt =  jwt.encode(to_encode , SECRET_KEY , algorithm= ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str,credentials_exception):
    try :
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)

        id : str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token : str  = Depends(oauth_scheme), db : Session = Depends(get_db)):
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate the credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token,credential_exception)
    user = db.query(User).filter(User.id == token.id).first()
    
    return user