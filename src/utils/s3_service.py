import aioboto3

from fastapi import HTTPException

from src.database.config import Config; (
    Config.AWS_ACCESS_KEY_ID,
    Config.AWS_SECRET_ACCESS_KEY,
    Config.AWS_BUCKET_NAME,
    Config.AWS_REGION,
    Config.CLOUDFRONT_URL
)


session = aioboto3.Session()


async def upload_image_to_s3(
    file_name: str,
    file_bytes: bytes,
    content_type: str = "image/jpeg"
):

    try:

        async with session.client(
            service_name="s3",
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        ) as s3_client:

            await s3_client.put_object(
                Bucket=Config.AWS_BUCKET_NAME,
                Key=file_name,
                Body=file_bytes,
                ContentType=content_type
            )

        image_url = (
            f"{Config.CLOUDFRONT_URL}/{file_name}"
        )

        return image_url

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"S3 Upload Failed: {str(error)}"
        )


async def delete_image_from_s3(
    image_url: str
):

    try:

        file_name = image_url.split("/", 3)[-1]

        async with session.client(
            service_name="s3",
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        ) as s3_client:

            await s3_client.delete_object(
                Bucket=Config.AWS_BUCKET_NAME,
                Key=file_name
            )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"S3 Delete Failed: {str(error)}"
        )