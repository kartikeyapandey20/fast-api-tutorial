from .repository import VoteRepository

class VoteDomain:
    def __init__(self) -> None:
        self.__repository = VoteRepository()
    
    def vote(self, vote, db, get_current_user):
        """
        Vote on a post.

        Args:
            vote: The vote data.
            db: The database session.
            get_current_user: The current authenticated user.

        Returns:
            dict: A message indicating the success of the operation.
        """
        return self.__repository.vote(vote, db, get_current_user)
