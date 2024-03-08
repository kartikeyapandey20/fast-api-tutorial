from fastapi import APIRouter
from api.v1.posts.router import PostRouter

api_router = APIRouter()

api_router.include_router(PostRouter().router)

@api_router.get("/")
def index():
	return {"status": "ok"}
