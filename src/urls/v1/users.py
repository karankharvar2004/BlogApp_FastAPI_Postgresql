from fastapi import (
    APIRouter,
    Depends
)

from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from src.database.db_config import get_db

from src.database.config import (
    SECRET_KEY,
    JWT_ALGORITHM
)

from src.services.users.controller import (
    register_user,
    login_user
)

from src.services.users.schema import (
    UserRegisterSchema,
    UserLoginSchema
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
    payload: UserRegisterSchema,
    db: AsyncSession = Depends(get_db)
):

    user = await register_user(
        payload,
        db
    )

    return success_response(
        message="User registered successfully",
        data={
            "id": user.id,
            "email": user.email
        },
        status_code=201
    )


@router.post("/login")
async def login(
    payload: UserLoginSchema,
    db: AsyncSession = Depends(get_db)
):

    token = await login_user(
        payload,
        db
    )

    return success_response(
        message="Login successful",
        data=token
    )


@router.post("/refresh-token")
async def refresh_token(
    token=Depends(security)
):

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
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

    return success_response(
        message="User profile fetched",
        data={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    )