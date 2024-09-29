import pytest
from quart import Quart


@pytest.mark.asyncio
async def test_control(app: Quart) -> None:
    test_client = app.test_client()
    response = await test_client.get("/control/ping/")
    assert (await response.get_json())["ping"] == "pong"
