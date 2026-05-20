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
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(Config.DATABASE_URL, future=True, echo=True)
        self._session = sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self):
        async_session = self._session()

        try:
            yield async_session
        finally:
            await async_session.close()


db = AsyncDatabaseSession()

db.init()


async def get_db():
    async for session in db.get_session():
        yield session