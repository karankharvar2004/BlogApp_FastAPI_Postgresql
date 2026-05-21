from dotenv import load_dotenv

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)

from src.database.config import Config


load_dotenv()


Base = declarative_base()


class AsyncDatabaseSession:

    def __init__(self):

        self._session = None

        self._engine = None

    def __getattr__(self, name):

        return getattr(
            self._session,
            name
        )

    def init(self):

        self._engine = create_async_engine(
            Config.DATABASE_URL,
            future=True,
            echo=True
        )

        async_session = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        self._session = async_session()

    async def close(self):

        if self._session:

            await self._session.close()


db = AsyncDatabaseSession()

db.init()


async def get_db():

    try:

        yield db

    finally:

        pass