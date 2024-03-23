from api.v1.posts.models import Post
from .schema import PostSchema
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException , status
from core.deps import get_db
from api.v1.auth.oauth2 import get_current_user 
from api.v1.user.models import User
from api.v1.vote.models import Voter
from sqlalchemy import func
class PostRepository:
    
    def get_post(self, db,get_current_user : User = Depends(get_current_user),limit : int = 10, skip : int = 0):
        
        posts = db.query(Post, func.count(Voter.post_id).label("votes")).join(
                Voter, Voter.post_id == Post.id, isouter=True).group_by(Post.id).limit(limit).offset(skip).all()
        serialized_posts = []
        for post, vote_count in posts:
            serialized_post = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "created_at": post.created_at,
                "owner_id": post.owner_id,
                "votes": vote_count
            }
            serialized_posts.append(serialized_post)
        
        return serialized_posts
    
    def create_post(self,post : PostSchema,db : Session = Depends(get_db),get_current_user : User = Depends(get_current_user)):
        new_posts = Post(owner_id=get_current_user.id ,**post.dict())
        db.add(new_posts)
        db.commit()
        db.refresh(new_posts)
        
        return new_posts
    
    def get_post_by_id(self, id , db : Session = Depends(get_db),get_current_user : User = Depends(get_current_user)):
        
        post = db.query(Post).filter(Post.id == id).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
        if post.owner_id!= get_current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized" 
            )
        return post
        
    def delete_post_by_id(self, id , db : Session = Depends(get_db),get_current_user : User = Depends(get_current_user)):
        
        post_query = db.query(Post).filter(Post.id == id)
        
        post = post_query.first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
        if post.owner_id!= get_current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized" 
            )
        post_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "post deleted successfully"}
    
    def update_post_by_id(self,id : int , updated_post : PostSchema,db : Session = Depends(get_db)):
        
        post_query = db.query(Post).filter(Post.id == id)

        post = post_query.first()
        
        if post == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
        if post.owner_id!= get_current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized" 
            )    
        post_query.update(updated_post.dict(),synchronize_session=False)
        db.commit()
        
        return post_query.first()