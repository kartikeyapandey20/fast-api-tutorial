from .repository import UserRepository

class UserDomain:
    
    def __init__(self) -> None:
        self.__repository = UserRepository()
        
    def create_user(self, db, user):
        return self.__repository.create_user(user,db)
    
    def get_user_by_id(self,id, db):
        return self.__repository.get_user_by_id(id,db)