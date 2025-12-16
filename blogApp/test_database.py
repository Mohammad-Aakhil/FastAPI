from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from blogApp.database import Base
from blogApp.core.config import settings

TEST_DATABASE_URL = settings.test_database_url
# sqlite+aiosqlite:///./test.db

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False
)

AsyncTestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def create_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
