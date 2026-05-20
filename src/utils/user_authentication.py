from datetime import datetime, timedelta

import jwt

from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.config import Config; (
    Config.SECRET_KEY,
    Config.JWT_ALGORITHM,
    Config.ACCESS_TOKEN_EXPIRE_MINUTES,
    Config.REFRESH_TOKEN_EXPIRE_DAYS
)

from src.database.db_config import get_db

from src.database.models import User


security = HTTPBearer()


def create_access_token(user_id: int):

    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def create_refresh_token(user_id: int):

    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(
            days=Config.REFRESH_TOKEN_EXPIRE_DAYS
        )
    }

    token = jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


async def get_current_user(
    token=Depends(security),
    db: AsyncSession = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token.credentials,
            Config.SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )

        if payload.get("type") != "access":

            raise HTTPException(
                status_code=401,
                detail="Invalid access token"
            )

        user_id = payload.get("user_id")

        query = select(User).where(
            User.id == user_id,
            User.is_deleted == False
        )

        result = await db.execute(query)

        user = result.scalar_one_or_none()

        if not user:

            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )