import pytest
from quart import Quart
from quart_auth import authenticated_client


async def test_post_todo(app: Quart) -> None:
    test_client = app.test_client()
    async with authenticated_client(test_client, "1"):  # type: ignore
        response = await test_client.post(
            "/todos/",
            json={"complete": False, "due": None, "task": "Test task"},
        )
        assert response.status_code == 201
        assert (await response.get_json())["id"] > 0


async def test_get_todo(app: Quart) -> None:
    test_client = app.test_client()
    async with authenticated_client(test_client, "1"):  # type: ignore
        response = await test_client.get("/todos/1/")
        assert response.status_code == 200
        assert (await response.get_json())["task"] == "Test Task"


@pytest.mark.parametrize(
    "complete, expected",
    [(True, 200), (False, 200), (None, 200)],
)
async def test_get_todos(app: Quart, complete: bool | None, expected: int) -> None:
    test_client = app.test_client()
    async with authenticated_client(test_client, "1"):  # type: ignore
        query_string = f"?complete={complete}" if complete is not None else ""
        response = await test_client.get(f"/todos/{query_string}")
        assert response.status_code == expected
        assert isinstance((await response.get_json())["todos"], list)


async def test_put_todo(app: Quart) -> None:
    test_client = app.test_client()
    async with authenticated_client(test_client, "1"):  # type: ignore
        response = await test_client.post(
            "/todos/",
            json={"complete": False, "due": None, "task": "Test task"},
        )
        todo_id = (await response.get_json())["id"]
        response = await test_client.put(
            f"/todos/{todo_id}/",
            json={"complete": False, "due": None, "task": "Updated"},
        )
        assert (await response.get_json())["task"] == "Updated"
        response = await test_client.get(f"/todos/{todo_id}/")
        assert (await response.get_json())["task"] == "Updated"


async def test_delete_todo(app: Quart) -> None:
    test_client = app.test_client()
    async with authenticated_client(test_client, "1"):  # type: ignore
        response = await test_client.post(
            "/todos/",
            json={"complete": False, "due": None, "task": "Test task"},
        )
        todo_id = (await response.get_json())["id"]
        await test_client.delete(f"/todos/{todo_id}/")
        response = await test_client.get(f"/todos/{todo_id}/")
        assert response.status_code == 404
