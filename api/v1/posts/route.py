from fastapi import APIRouter , Depends , status
from .domain import PostDomain
from sqlalchemy.orm import Session
from core.deps import get_db
from .schema import PostSchema , Post , PostVote
from .models import Post as PostModel
from api.v1.auth.oauth2 import get_current_user
from sqlalchemy import func
from api.v1.vote.models import Voter
class PostRouter:
    def __init__(self) -> None:
        self.__domain = PostDomain()
    
    @property
    def router(self):
        api_router = APIRouter(prefix="/posts",tags=["post"])
        
        @api_router.get("/",status_code=status.HTTP_200_OK,response_model=list[PostVote])
        def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0):
            return self.__domain.get_post(db,current_user,limit,skip)

        
        @api_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Post)
        def create_post(post : PostSchema ,db : Session = Depends(get_db),get_current_user : int = Depends(get_current_user)):
            return self.__domain.create_post(db, post,get_current_user)
        
        @api_router.get("/{id}",response_model=Post)
        def get_post_by_id(id : int ,db : Session = Depends(get_db),get_current_user : int = Depends(get_current_user)):
            return self.__domain.get_post_by_id(id,db,get_current_user)
        
        @api_router.delete("/{id}")
        def update_post_by_id(id : int,db : Session = Depends(get_db),get_current_user : int = Depends(get_current_user)): 
            return self.__domain.delete_post_by_id(id,db,get_current_user)        

        @api_router.put("/{id}",response_model=Post)
        def update_post_by_id(id : int,post : PostSchema ,db : Session = Depends(get_db)): 
            return self.__domain.update_post_by_id(id,post,db)
        
        return api_router