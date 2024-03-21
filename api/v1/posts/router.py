from fastapi import APIRouter , Depends , status
from .domain import PostDomain
from sqlalchemy.orm import Session
from core.deps import get_db
from .schema import PostSchema , Post
class PostRouter:
    def __init__(self) -> None:
        self.__domain = PostDomain()
    
    @property
    def router(self):
        api_router = APIRouter(prefix="/posts",tags=["post"])
        
        @api_router.get("/",status_code=status.HTTP_200_OK,response_model=list[Post])
        def get_posts(db : Session = Depends(get_db)):
            return self.__domain.get_post(db)
        
        @api_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Post)
        def create_post(post : PostSchema ,db : Session = Depends(get_db)):
            return self.__domain.create_post(db, post)
        
        @api_router.get("/{id}",response_model=Post)
        def get_post_by_id(id : int ,db : Session = Depends(get_db)):
            return self.__domain.get_post_by_id(id,db)
        
        @api_router.put("/{id}",response_model=Post)
        def update_post_by_id(id : int,post : PostSchema ,db : Session = Depends(get_db)): 
            return self.__domain.update_post_by_id(id,post,db)
        
        return api_router