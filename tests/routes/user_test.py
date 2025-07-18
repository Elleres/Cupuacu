import pytest


@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    async for client in async_client:
        response = await client.get(
            "/",
        )
        data = response.json()
        assert data == {'detail': 'Not Found'}