from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class CreateBlogSchema(BaseModel):

    title: Annotated[
        str,
        Field(
            min_length=3,
            max_length=255
        )
    ]

    content: Annotated[
        str,
        Field(
            min_length=3
        )
    ]

    image_base64: Annotated[
        str | None,
        Field(default=None)
    ]


class UpdateBlogSchema(BaseModel):

    title: Annotated[
        str | None,
        Field(
            default=None,
            min_length=3,
            max_length=255
        )
    ]

    content: Annotated[
        str | None,
        Field(
            default=None,
            min_length=3
        )
    ]

    image_base64: Annotated[
        str | None,
        Field(default=None)
    ]


class BlogResponseSerializer(BaseModel):

    id: int

    title: str

    content: str

    image_url: str | None

    owner_id: int

    model_config = ConfigDict(
        from_attributes=True
    )