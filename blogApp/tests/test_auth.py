import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_login_success(client, test_user):
    response = await client.post(
        "/login",
        data={
            "username": test_user.name,
            "password": "password",
            # "grant_type": "password"
              },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
            }
            )
    assert response.status_code == 202

    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post(
        "/login",
        data={
            "name": "wrong",
            "password": "wrong",
        }
    )

    assert response.status_code in (422, 401)