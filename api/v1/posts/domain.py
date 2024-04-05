from .repository import PostRepository
from .schema import PostSchema

class PostDomain:
    def __init__(self) -> None:
        self.__repository = PostRepository()
        
    def get_post(self, db, get_current_user, limit, skip):
        """
        Get a list of posts.

        Args:
            db: The database session.
            get_current_user: The current authenticated user.
            limit: The maximum number of posts to retrieve.
            skip: The number of posts to skip.

        Returns:
            list: A list of serialized posts.
        """
        return self.__repository.get_post(db, get_current_user, limit, skip)
    
    def create_post(self, db, post: PostSchema, get_current_user):
        """
        Create a new post.

        Args:
            db: The database session.
            post (PostSchema): The data for the new post.
            get_current_user: The current authenticated user.

        Returns:
            Post: The newly created post.
        """
        return self.__repository.create_post(db, post, get_current_user)
    
    def get_post_by_id(self, id, db, get_current_user):
        """
        Get a post by its ID.

        Args:
            id: The ID of the post.
            db: The database session.
            get_current_user: The current authenticated user.

        Returns:
            dict: A serialized representation of the post.
        """
        return self.__repository.get_post_by_id(id, db, get_current_user)
    
    def delete_post_by_id(self, id, db, get_current_user):
        """
        Delete a post by its ID.

        Args:
            id: The ID of the post to delete.
            db: The database session.
            get_current_user: The current authenticated user.

        Returns:
            dict: A message indicating the success of the deletion.
        """
        return self.__repository.delete_post_by_id(id, db, get_current_user)
    
    def update_post_by_id(self, id, post, db, get_current_user):
        """
        Update a post by its ID.

        Args:
            id: The ID of the post to update.
            post: The updated data for the post.
            db: The database session.
            get_current_user: The current authenticated user.

        Returns:
            Post: The updated post.
        """
        return self.__repository.update_post_by_id(id, post, db, get_current_user)
