from fastapi import APIRouter

from src.urls.v1.users import (
    router as users_router
)

from src.urls.v1.blogs import (
    router as blogs_router
)


api_router = APIRouter()

api_router.include_router(
    users_router
)

api_router.include_router(
    blogs_router
)