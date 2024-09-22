import pytest
from quart import Quart


@pytest.mark.asyncio
async def test_control(test_app: Quart) -> None:
    test_client = test_app.test_client()
    response = await test_client.get("/control/ping/")
    assert (await response.get_json())["ping"] == "pong"
