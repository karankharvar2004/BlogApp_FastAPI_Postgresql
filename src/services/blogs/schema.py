from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


TitleField = Annotated[
    str,
    Field(
        min_length=3,
        max_length=255,
        examples=["My First Blog"]
    )
]


ContentField = Annotated[
    str,
    Field(
        min_length=10,
        examples=["This is my blog content"]
    )
]


Base64ImageField = Annotated[
    str | None,
    Field(
        default=None,
        examples=["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."]
    )
]


class CreateBlogSchema(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    title: TitleField

    content: ContentField

    image_base64: Base64ImageField = None


class UpdateBlogSchema(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    title: Annotated[
        str | None,
        Field(
            min_length=3,
            max_length=255,
            default=None
        )
    ] = None

    content: Annotated[
        str | None,
        Field(
            min_length=10,
            default=None
        )
    ] = None

    image_base64: Base64ImageField = None