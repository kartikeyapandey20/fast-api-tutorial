from api.v1.posts.models import Post
from .schema import PostSchema
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException , status
from core.deps import get_db
class PostRepository:
    
    def get_post(self, db):
        
        posts =  db.query(Post).all()
        
        return posts
    
    def create_post(self,post : PostSchema,db : Session = Depends(get_db)):
        new_posts = Post(**post.dict())
        db.add(new_posts)
        db.commit()
        db.refresh(new_posts)
        
        return new_posts
    
    def get_post_by_id(self, id , db : Session = Depends(get_db)):
        
        post = db.query(Post).filter(Post.id == id).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
        return post
        
    def delete_post_by_id(self, id , db : Session = Depends(get_db)):
        
        post = db.query(Post).filter(Post.id == id)
        
        if not post.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
            
        post.delete(synchronize_session=False)
        db.commit()
        
        return post
    
    def update_post_by_id(self,id : int , updated_post : PostSchema,db : Session = Depends(get_db)):
        
        post_query = db.query(Post).filter(Post.id == id)

        post = post_query.first()
        
        if post == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
            
        post_query.update(updated_post.dict(),synchronize_session=False)
        db.commit()
        
        return post_query.first()