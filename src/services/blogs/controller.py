from fastapi import status

from src.services.blogs.schema import BlogSchema

from src.services.blogs.serializer import (
    BlogResponseSerializer
)

from src.utils.helper_functions import (
    decode_base64_image
)

from src.utils.s3_service import (
    upload_image_to_s3,
    delete_image_from_s3
)

from src.utils.response import (
    success_response,
    error_response
)


class BlogController:

    @classmethod
    async def create_blog(
        cls,
        request,
        current_user
    ):

        image_url = None

        if request.image_base64:

            image_data = decode_base64_image(
                request.image_base64
            )

            image_url = await upload_image_to_s3(
                file_name=image_data["file_name"],
                file_bytes=image_data["file_bytes"]
            )

        blog = await BlogSchema.create_blog(
            request=request,
            current_user=current_user,
            image_url=image_url
        )

        response_data = BlogResponseSerializer.model_validate(
            blog
        )

        return success_response(
            message="Blog created successfully",
            data=response_data.model_dump(),
            status_code=status.HTTP_201_CREATED
        )

    @classmethod
    async def get_all_blogs(
        cls
    ):

        blogs = await BlogSchema.get_blog_data()

        response_data = [
            BlogResponseSerializer
            .model_validate(blog)
            .model_dump()
            for blog in blogs
        ]

        return success_response(
            message="Blogs fetched successfully",
            data=response_data
        )

    @classmethod
    async def get_single_blog(
        cls,
        blog_id
    ):

        blog = await BlogSchema.get_blog_data(
            blog_id=blog_id
        )

        if not blog:

            return error_response(
                message="Blog not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        response_data = BlogResponseSerializer.model_validate(
            blog
        )

        return success_response(
            message="Blog fetched successfully",
            data=response_data.model_dump()
        )

    @classmethod
    async def update_blog(
        cls,
        blog_id,
        request,
        current_user
    ):

        blog = await BlogSchema.get_blog_data(
            blog_id=blog_id
        )

        if not blog:

            return error_response(
                message="Blog not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if blog.owner_id != current_user.id:

            return error_response(
                message="Not authorized",
                status_code=status.HTTP_403_FORBIDDEN
            )

        image_url = blog.image_url

        if request.image_base64 is not None:

            if blog.image_url:

                await delete_image_from_s3(
                    blog.image_url
                )

            image_data = decode_base64_image(
                request.image_base64
            )

            image_url = await upload_image_to_s3(
                file_name=image_data["file_name"],
                file_bytes=image_data["file_bytes"]
            )

        updated_blog = await BlogSchema.update_blog(
            blog=blog,
            request=request,
            image_url=image_url
        )

        response_data = BlogResponseSerializer.model_validate(
            updated_blog
        )

        return success_response(
            message="Blog updated successfully",
            data=response_data.model_dump()
        )

    @classmethod
    async def delete_blog(
        cls,
        blog_id,
        current_user
    ):

        blog = await BlogSchema.get_blog_data(
            blog_id=blog_id
        )

        if not blog:

            return error_response(
                message="Blog not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if blog.owner_id != current_user.id:

            return error_response(
                message="Not authorized",
                status_code=status.HTTP_403_FORBIDDEN
            )

        if blog.image_url:

            await delete_image_from_s3(
                blog.image_url
            )

        await BlogSchema.soft_delete_blog(
            blog
        )

        return success_response(
            message="Blog deleted successfully"
        )