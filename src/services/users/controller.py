from fastapi import status

from src.services.users.schema import UserSchema

from src.services.users.serializer import (
    UserResponseSerializer,
    UserProfileSerializer
)

from src.utils.helper_functions import (
    hash_password,
    verify_password
)

from src.utils.user_authentication import (
    create_access_token,
    create_refresh_token
)

from src.utils.response import (
    success_response,
    error_response
)


class UserController:

    @classmethod
    async def register_user(
        cls,
        request
    ):

        existing_user = await UserSchema.get_user_data(
            email=request.email
        )

        if existing_user:

            return error_response(
                message="Email already exists",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        request.password = hash_password(
            request.password
        )

        user = await UserSchema.create_user(
            request=request
        )

        response_data = UserProfileSerializer.model_validate(
            user
        )

        return success_response(
            message="User registered successfully",
            data=response_data.model_dump(),
            status_code=status.HTTP_201_CREATED
        )

    @classmethod
    async def login_user(
        cls,
        request
    ):

        user = await UserSchema.get_user_data(
            email=request.email
        )

        if not user:

            return error_response(
                message="Invalid credentials",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        valid_password = verify_password(
            request.password,
            user.password
        )

        if not valid_password:

            return error_response(
                message="Invalid credentials",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        access_token = create_access_token(
            user.id
        )

        refresh_token = create_refresh_token(
            user.id
        )

        response_data = UserResponseSerializer(
            id=user.id,
            username=user.username,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token
        )

        return success_response(
            message="Login successful",
            data=response_data.model_dump()
        )

    @classmethod
    async def get_profile(
        cls,
        current_user
    ):

        response_data = UserProfileSerializer.model_validate(
            current_user
        )

        return success_response(
            message="User profile fetched",
            data=response_data.model_dump()
        )