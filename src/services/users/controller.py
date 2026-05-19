from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import User

from src.utils.helper_functions import (
    hash_password,
    verify_password
)

from src.utils.user_authentication import (
    create_access_token,
    create_refresh_token
)


async def register_user(
    payload,
    db: AsyncSession
):

    query = select(User).where(
        User.email == payload.email
    )

    result = await db.execute(query)

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password)
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return new_user


async def login_user(
    payload,
    db: AsyncSession
):

    query = select(User).where(
        User.email == payload.email
    )

    result = await db.execute(query)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    if not verify_password(
        payload.password,
        user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    access_token = create_access_token(user.id)

    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
