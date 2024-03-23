from .schema import Vote
from fastapi import Depends , HTTPException ,status
from sqlalchemy.orm import Session
from api.v1.auth.oauth2 import get_current_user
from core.deps import get_db
from .models import Voter
from api.v1.posts.models import Post
class VoteRepository:
    def vote(self,vote : Vote , db : Session = Depends(get_db), get_current_user : Session = Depends(get_current_user)):
        
        post = db.query(Post).filter(Post.id == vote.post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post does not exist"
            )
            
        vote_query = db.query(Voter).filter(Voter.post_id == vote.post_id , Voter.user_id == get_current_user.id)
    
        found_vote = vote_query.first()
        if(vote.dir == 1):
            if(found_vote):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="You have already voted for this post"
                )
            new_vote = Voter(post_id=vote.post_id ,user_id=get_current_user.id)
            db.add(new_vote)
            db.commit()
            
            return {"message" : "successfully added vote"}
        else:
            if not found_vote:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Vote Does not exist"
                )
            vote_query.delete(synchronize_session=False)
            db.commit()
            
            return {"message": "successfully deleted vote"} 