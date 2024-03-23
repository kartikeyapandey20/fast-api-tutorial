from db.database import Base 
from sqlalchemy import Integer , Column , ForeignKey

class Voter(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
