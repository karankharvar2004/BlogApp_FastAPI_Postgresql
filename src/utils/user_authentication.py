from datetime import datetime, timedelta

import jwt

from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

from src.database.db_config import get_db

from src.database.models import User


security = HTTPBearer()


def create_access_token(user_id: int):

    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token


def create_refresh_token(user_id: int):

    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token


async def get_current_user(
    token=Depends(security),
    db: AsyncSession = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
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