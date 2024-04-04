from .repository import AuthenticationRepository

class AuthenticationDomain:
    def __init__(self) -> None:
        self.__repository = AuthenticationRepository()
        
    def login(self, user_credentials , db):
        return self.__repository.login(user_credentials , db)