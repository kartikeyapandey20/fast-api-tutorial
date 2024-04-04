from .repository import PostRepository
from .schema import PostSchema
class PostDomain:
    
    def __init__(self) -> None:
        self.__repository = PostRepository()
        
    def get_post(self , db,get_current_user,limit,skip):
        return self.__repository.get_post(db,get_current_user,limit,skip)
    
    def create_post(self,db,post : PostSchema , get_current_user):
        return self.__repository.create_post(post,db,get_current_user)
    
    def get_post_by_id(self,id ,db,get_current_user):
        return self.__repository.get_post_by_id(id,db,get_current_user)
    def delete_post_by_id(self,id,db,get_current_user):
        return self.__repository.delete_post_by_id(id,db,get_current_user)
    def update_post_by_id(self,id,post,db,get_current_user):
        return self.__repository.update_post_by_id(id,post,db,get_current_user)