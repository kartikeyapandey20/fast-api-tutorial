from fastapi import APIRouter
from api.v1.posts.route import PostRouter
from api.v1.user.route import UserRouter
from api.v1.auth.route import AuthenticationRouter
api_router = APIRouter()

api_router.include_router(PostRouter().router)
api_router.include_router(UserRouter().router)
api_router.include_router(AuthenticationRouter().router)

@api_router.get("/")
def index():
	return {"status": "ok"}
