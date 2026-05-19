from typing import Annotated

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict
)


UsernameField = Annotated[
    str,
    Field(
        min_length=3,
        max_length=50,
        examples=["karan"]
    )
]


EmailField = Annotated[
    EmailStr,
    Field(
        examples=["karan@gmail.com"]
    )
]


PasswordField = Annotated[
    str,
    Field(
        min_length=6,
        max_length=100,
        examples=["strongpassword123"]
    )
]


class UserRegisterSchema(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    username: UsernameField

    email: EmailField

    password: PasswordField


class UserLoginSchema(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    email: EmailField

    password: PasswordField