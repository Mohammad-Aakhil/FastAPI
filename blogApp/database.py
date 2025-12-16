from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from blogApp.core.config import settings
DATABASE_URL = "postgresql+asyncpg://postgres:00001234@localhost:5432/cleandb"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine,
                            expire_on_commit=False,
                            class_=AsyncSession)

Base = declarative_base()



async def get_db():
    async with SessionLocal() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
            