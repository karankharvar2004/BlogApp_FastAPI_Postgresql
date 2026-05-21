from datetime import datetime

from sqlalchemy import select

from src.database.models import Blog
from src.database.db_config import db


class BlogSchema:

    @classmethod
    async def create_blog(
        cls,
        request,
        current_user,
        image_url
    ):

        new_blog = Blog(
            title=request.title,
            content=request.content,
            image_url=image_url,
            owner_id=current_user.id
        )

        db.add(new_blog)

        await db.commit()

        await db.refresh(new_blog)

        return new_blog

    @classmethod
    async def get_blog_data(
        cls,
        blog_id=None
    ):

        query = select(Blog).where(
            Blog.is_deleted == False
        )

        if blog_id:

            query = query.where(
                Blog.id == blog_id
            )

        result = await db.execute(query)

        if blog_id:

            return result.scalar_one_or_none()

        return result.scalars().all()

    @classmethod
    async def update_blog(
        cls,
        blog,
        request,
        image_url=None
    ):

        if request.title is not None:

            blog.title = request.title

        if request.content is not None:

            blog.content = request.content

        if image_url is not None:

            blog.image_url = image_url

        blog.updated_at = datetime.utcnow()

        await db.commit()

        await db.refresh(blog)

        return blog

    @classmethod
    async def soft_delete_blog(
        cls,
        blog
    ):

        blog.is_deleted = True

        blog.deleted_at = datetime.utcnow()

        await db.commit()

        return True