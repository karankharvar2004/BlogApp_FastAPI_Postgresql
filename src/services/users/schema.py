from sqlalchemy import select

from src.database.models import User
from src.database.db_config import db


class UserSchema:

    @classmethod
    async def get_user_data(
        cls,
        user_id=None,
        email=None
    ):

        query = select(User)

        if user_id:

            query = query.where(
                User.id == user_id
            )

        if email:

            query = query.where(
                User.email == email
            )

        result = await db.execute(query)

        if user_id or email:

            return result.scalar_one_or_none()

        return result.scalars().all()

    @classmethod
    async def create_user(
        cls,
        request
    ):

        new_user = User(
            username=request.username,
            email=request.email,
            password=request.password
        )

        db.add(new_user)

        await db.commit()

        await db.refresh(new_user)

        return new_user