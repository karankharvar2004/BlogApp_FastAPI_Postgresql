from fastapi import (
    APIRouter,
    Depends
)

from fastapi.security import HTTPBearer

import jwt

from src.database.config import Config

from src.services.users.serializer import (
    UserRegisterSerializer,
    UserLoginSerializer
)

from src.services.users.controller import (
    UserController
)

from src.utils.user_authentication import (
    get_current_user,
    create_access_token
)

from src.utils.response import (
    success_response,
    error_response
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


security = HTTPBearer()


@router.post("/register")
async def register(
    request: UserRegisterSerializer
):

    return await UserController.register_user(
        request=request
    )


@router.post("/login")
async def login(
    request: UserLoginSerializer
):

    return await UserController.login_user(
        request=request
    )


@router.post("/refresh-token")
async def refresh_token(
    token=Depends(security)
):

    try:

        payload = jwt.decode(
            token.credentials,
            Config.SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )

        if payload.get("type") != "refresh":

            return error_response(
                message="Invalid refresh token",
                status_code=401
            )

        user_id = payload.get("user_id")

        new_access_token = create_access_token(
            user_id
        )

        return success_response(
            message="New access token generated",
            data={
                "access_token": new_access_token
            }
        )

    except Exception:

        return error_response(
            message="Refresh token expired",
            status_code=401
        )


@router.get("/me")
async def get_profile(
    current_user=Depends(get_current_user)
):

    return await UserController.get_profile(
        current_user=current_user
    )