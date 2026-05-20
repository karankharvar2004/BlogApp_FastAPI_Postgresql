import base64
import uuid

from io import BytesIO

from PIL import Image

from fastapi import HTTPException

from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


ALLOWED_IMAGE_TYPES = [
    "JPEG",
    "PNG",
    "WEBP"
]


def decode_base64_image(
    image_base64: str
):

    try:

        if "," in image_base64:

            image_base64 = image_base64.split(",")[1]

        image_bytes = base64.b64decode(
            image_base64
        )

        image = Image.open(
            BytesIO(image_bytes)
        )

        image.verify()

        image = Image.open(
            BytesIO(image_bytes)
        )

        image_format = image.format

        if image_format not in ALLOWED_IMAGE_TYPES:

            raise HTTPException(
                status_code=400,
                detail="Unsupported image type"
            )

        extension = image_format.lower()

        file_name = f"{uuid.uuid4()}.{extension}"

        return {
            "file_name": file_name,
            "file_bytes": image_bytes
        }

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid base64 image"
        )