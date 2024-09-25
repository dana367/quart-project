from typing import AsyncGenerator

import pytest
from quart import Quart
from quart_db import Connection

from backend.run import app, quart_db


@pytest.fixture(name="test_app", scope="function")
async def _test_app() -> AsyncGenerator[Quart, None]:
    async with app.test_app() as test_app:
        yield test_app


@pytest.fixture(name="connection", scope="function")
async def _connection(test_app: Quart) -> AsyncGenerator[Connection, None]:
    async with quart_db.connection() as connection:
        async with connection.transaction():
            yield connection
