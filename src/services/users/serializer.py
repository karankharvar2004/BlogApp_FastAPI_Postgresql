from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


UsernameField = Annotated[str, Field(min_length=3, max_length=50, examples=["karan"])]
EmailField = Annotated[EmailStr, Field(examples=["karan@gmail.com"])]
PasswordField = Annotated[str, Field(min_length=6, max_length=100, examples=["strongpassword123"])]


class UserRegisterSerializer(BaseModel):

    model_config = ConfigDict(extra="forbid",from_attributes=True)

    username: UsernameField
    email: EmailField
    password: PasswordField


class UserLoginSerializer(BaseModel):

    model_config = ConfigDict(extra="forbid",from_attributes=True)

    email: EmailField
    password: PasswordField


class UserResponseSerializer(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    access_token: str
    refresh_token: str


class UserProfileSerializer(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr