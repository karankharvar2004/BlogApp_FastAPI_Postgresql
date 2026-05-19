from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db

from src.services.blogs.schema import (
    CreateBlogSchema,
    UpdateBlogSchema
)

from src.services.blogs.controller import (
    create_blog,
    get_all_blogs,
    get_single_blog,
    update_blog,
    delete_blog
)

from src.services.blogs.serializer import (
    BlogResponseSerializer
)

from src.utils.user_authentication import (
    get_current_user
)

from src.utils.response import (
    success_response
)


router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


@router.post("/")
async def create_new_blog(
    payload: CreateBlogSchema,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    blog = await create_blog(
        payload,
        current_user,
        db
    )

    serialized_blog = (
        BlogResponseSerializer
        .model_validate(blog)
        .model_dump()
    )

    return success_response(
        message="Blog created successfully",
        data=serialized_blog
    )


@router.get("/")
async def fetch_all_blogs(
    db: AsyncSession = Depends(get_db)
):

    blogs = await get_all_blogs(db)

    serialized_blogs = [
        BlogResponseSerializer
        .model_validate(blog)
        .model_dump()
        for blog in blogs
    ]

    return success_response(
        message="Blogs fetched successfully",
        data=serialized_blogs
    )


@router.get("/{blog_id}")
async def fetch_single_blog(
    blog_id: int,
    db: AsyncSession = Depends(get_db)
):

    blog = await get_single_blog(
        blog_id,
        db
    )

    serialized_blog = (
        BlogResponseSerializer
        .model_validate(blog)
        .model_dump()
    )

    return success_response(
        message="Blog fetched successfully",
        data=serialized_blog
    )


@router.patch("/{blog_id}")
async def partial_update_blog(
    blog_id: int,
    payload: UpdateBlogSchema,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    blog = await update_blog(
        blog_id,
        payload,
        current_user,
        db
    )

    serialized_blog = (
        BlogResponseSerializer
        .model_validate(blog)
        .model_dump()
    )

    return success_response(
        message="Blog updated successfully",
        data=serialized_blog
    )


@router.delete("/{blog_id}")
async def remove_blog(
    blog_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    await delete_blog(
        blog_id,
        current_user,
        db
    )

    return success_response(
        message="Blog deleted successfully"
    )