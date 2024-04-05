from .domain import VoteDomain
from fastapi import APIRouter, Depends, status
from .schema import Vote
from sqlalchemy.orm import Session
from core.deps import get_db
from api.v1.auth.oauth2 import get_current_user

class VoteRouter:
    def __init__(self) -> None:
        self.__domain = VoteDomain()
    
    @property
    def router(self):
        """
        Get the API router for votes.

        Returns:
            APIRouter: The API router.
        """
        api_router = APIRouter(prefix="/vote", tags=["vote"])
        
        @api_router.post("/", status_code=status.HTTP_201_CREATED)
        def vote(vote: Vote, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
            """
            Vote on a post.

            Args:
                vote (Vote): The vote data.
                db (Session): The database session.
                get_current_user (int): The current authenticated user ID.

            Returns:
                dict: A message indicating the success of the operation.
            """
            return self.__domain.vote(vote, db, get_current_user)
        
        return api_router
