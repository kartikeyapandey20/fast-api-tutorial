from fastapi import APIRouter , Depends
from .domain import PostDomain
from sqlalchemy.orm import Session
from core.deps import get_db
from .schema import PostSchema
class PostRouter:
    def __init__(self) -> None:
        self.__domain = PostDomain()
    
    @property
    def router(self):
        api_router = APIRouter(prefix="/posts",tags=["post"])
        
        @api_router.get("/")
        def get_posts(db : Session = Depends(get_db)):
            return self.__domain.get_post(db)
        
        @api_router.post("/")
        def create_post(post : PostSchema ,db : Session = Depends(get_db)):
            return self.__domain.create_post(db, post)
        
        @api_router.get("/{id}")
        def get_post_by_id(id : int ,db : Session = Depends(get_db)):
            return self.__domain.get_post_by_id(id,db)
        
        @api_router.put("/{id}")
        def update_post_by_id(id : int,post : PostSchema ,db : Session = Depends(get_db)): 
            return self.__domain.update_post_by_id(id,post,db)
        
        return api_router