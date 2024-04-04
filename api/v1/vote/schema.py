from pydantic import BaseModel , conint

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)