from .repository import PostRepository
from .schema import PostSchema
class PostDomain:
    
    def __init__(self) -> None:
        self.__repository = PostRepository()
        
    def get_post(self , db):
        return self.__repository.get_post(db)
    
    def create_post(self,db,post : PostSchema):
        return self.__repository.create_post(post,db)
    
    def get_post_by_id(self,id ,db):
        return self.__repository.get_post_by_id(id,db)
    def delete_post_by_id(self,id,db):
        return self.__repository.delete_post_by_id(id,db)
        return self.__repository.get_post_by_id(id,db)
    def update_post_by_id(self,id,post,db):
        return self.__repository.update_post_by_id(id,post,db)