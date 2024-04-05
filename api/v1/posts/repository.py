from api.v1.posts.models import Post
from .schema import PostSchema
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from core.deps import get_db
from api.v1.auth.oauth2 import get_current_user 
from api.v1.user.models import User
from api.v1.vote.models import Voter
from sqlalchemy import func

class PostRepository:
    
    def get_post(self, db: Session, get_current_user: User = Depends(get_current_user), limit: int = 10, skip: int = 0):
        """
        Get a list of posts.

        Args:
            db (Session): The SQLAlchemy database session.
            get_current_user (User): The current authenticated user.
            limit (int): The maximum number of posts to retrieve.
            skip (int): The number of posts to skip.

        Returns:
            list: A list of serialized posts.
        """
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
    
    def create_post(self, post: PostSchema, db: Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
        """
        Create a new post.

        Args:
            post (PostSchema): The data for the new post.
            db (Session): The SQLAlchemy database session.
            get_current_user (User): The current authenticated user.

        Returns:
            Post: The newly created post.
        """
        new_post = Post(owner_id=get_current_user.id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        return new_post
    
    def get_post_by_id(self, id, db: Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
        """
        Get a post by its ID.

        Args:
            id (int): The ID of the post.
            db (Session): The SQLAlchemy database session.
            get_current_user (User): The current authenticated user.

        Raises:
            HTTPException: If the post is not found.

        Returns:
            dict: A serialized representation of the post.
        """
        posts = db.query(Post, func.count(Voter.post_id).label("votes")).join(
        Voter, Voter.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.id == id).first()
        
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
        post, votes = posts
        serialized_post = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "created_at": post.created_at,
            "owner_id": post.owner_id,
            "votes": votes
            }
        return serialized_post
        
    def delete_post_by_id(self, id, db: Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
        """
        Delete a post by its ID.

        Args:
            id (int): The ID of the post to delete.
            db (Session): The SQLAlchemy database session.
            get_current_user (User): The current authenticated user.

        Raises:
            HTTPException: If the post is not found or the user is not authorized.

        Returns:
            dict: A message indicating the success of the deletion.
        """
        post_query = db.query(Post).filter(Post.id == id)
        
        post = post_query.first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
        if post.owner_id != get_current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized" 
            )
        post_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "Post deleted successfully"}
    
    def update_post_by_id(self, id: int, updated_post: PostSchema, db: Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
        """
        Update a post by its ID.

        Args:
            id (int): The ID of the post to update.
            updated_post (PostSchema): The updated data for the post.
            db (Session): The SQLAlchemy database session.
            get_current_user (User): The current authenticated user.

        Raises:
            HTTPException: If the post is not found or the user is not authorized.

        Returns:
            Post: The updated post.
        """
        post_query = db.query(Post).filter(Post.id == id)

        post = post_query.first()
        
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found" 
            )
        if post.owner_id != get_current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized" 
            )    
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()
        
        return post_query.first()
