from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import Blog

from src.utils.helper_functions import (
    decode_base64_image
)

from src.utils.s3_service import (
    upload_image_to_s3,
    delete_image_from_s3
)


async def create_blog(
    payload,
    current_user,
    db: AsyncSession
):

    image_url = None

    if payload.image_base64:

        image_data = decode_base64_image(
            payload.image_base64
        )

        image_url = await upload_image_to_s3(
            file_name=image_data["file_name"],
            file_bytes=image_data["file_bytes"]
            )
    
    new_blog = Blog(
        title=payload.title,
        content=payload.content,
        image_url=image_url,
        owner_id=current_user.id
    )

    db.add(new_blog)

    await db.commit()

    await db.refresh(new_blog)

    return new_blog


async def get_all_blogs(
    db: AsyncSession
):

    query = select(Blog).where(
        Blog.is_deleted == False
    )

    result = await db.execute(query)

    blogs = result.scalars().all()

    return blogs


async def get_single_blog(
    blog_id: int,
    db: AsyncSession
):

    query = select(Blog).where(
        Blog.id == blog_id,
        Blog.is_deleted == False
    )

    result = await db.execute(query)

    blog = result.scalar_one_or_none()

    if not blog:

        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return blog


async def update_blog(
    blog_id: int,
    payload,
    current_user,
    db: AsyncSession
):

    query = select(Blog).where(
        Blog.id == blog_id,
        Blog.is_deleted == False
    )

    result = await db.execute(query)

    blog = result.scalar_one_or_none()

    if not blog:

        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    if blog.owner_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if payload.title is not None:

        blog.title = payload.title

    if payload.content is not None:

        blog.content = payload.content

    if payload.image_base64 is not None:

        if blog.image_url:

            await delete_image_from_s3(
                blog.image_url
            )

        image_data = decode_base64_image(
            payload.image_base64
        )

        blog.image_url = await upload_image_to_s3(
            file_name=image_data["file_name"],
            file_bytes=image_data["file_bytes"]
        )

    blog.updated_at = datetime.utcnow()

    await db.commit()

    await db.refresh(blog)

    return blog


async def delete_blog(
    blog_id: int,
    current_user,
    db: AsyncSession
):

    query = select(Blog).where(
        Blog.id == blog_id,
        Blog.is_deleted == False
    )

    result = await db.execute(query)

    blog = result.scalar_one_or_none()

    if not blog:

        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    if blog.owner_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    
    if blog.image_url:

        await delete_image_from_s3(
            blog.image_url
        )

    blog.is_deleted = True

    blog.deleted_at = datetime.utcnow()

    await db.commit()

    return True