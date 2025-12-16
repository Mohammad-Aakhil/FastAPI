import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from blogApp.main import app
from blogApp.database import get_db
from blogApp.test_database import AsyncTestingSessionLocal, create_test_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    await create_test_db()

async def override_get_db():
    async with AsyncTestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport = transport,
        base_url="http://test"
    ) as ac:
        yield ac

import pytest
from blogApp.models import User
from blogApp.hashing import Hash
from blogApp.test_database import AsyncTestingSessionLocal


@pytest_asyncio.fixture
async def test_user():
    async with AsyncTestingSessionLocal() as session:
        await session.execute(text("DELETE FROM users"))

        user = User(
            name="testuser",
            password=Hash.argon2("password"),
            role="user"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    