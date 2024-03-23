from .repository import VoteRepository

class VoteDomain:
    def __init__(self) -> None:
        self.__repository = VoteRepository()
    
    def vote(self, vote,db,get_current_user):
        return self.__repository.vote(vote,db,get_current_user)

