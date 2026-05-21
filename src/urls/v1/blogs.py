from fastapi import (
    APIRouter,
    Depends
)

from src.services.blogs.serializer import (
    CreateBlogSerializer,
    UpdateBlogSerializer
)

from src.services.blogs.controller import (
    BlogController
)

from src.utils.user_authentication import (
    get_current_user
)


router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


@router.post("/")
async def create_new_blog(
    request: CreateBlogSerializer,
    current_user=Depends(get_current_user)
):

    return await BlogController.create_blog(
        request=request,
        current_user=current_user
    )


@router.get("/")
async def fetch_all_blogs():

    return await BlogController.get_all_blogs()


@router.get("/{blog_id}")
async def fetch_single_blog(
    blog_id: int
):

    return await BlogController.get_single_blog(
        blog_id=blog_id
    )


@router.patch("/{blog_id}")
async def partial_update_blog(
    blog_id: int,
    request: UpdateBlogSerializer,
    current_user=Depends(get_current_user)
):

    return await BlogController.update_blog(
        blog_id=blog_id,
        request=request,
        current_user=current_user
    )


@router.delete("/{blog_id}")
async def remove_blog(
    blog_id: int,
    current_user=Depends(get_current_user)
):

    return await BlogController.delete_blog(
        blog_id=blog_id,
        current_user=current_user
    )