from quart import Quart
from quart import ResponseReturnValue
from quart_db import QuartDB
import os
from subprocess import call  # nosec
from urllib.parse import urlparse

app = Quart(__name__)
app.config.from_prefixed_env(prefix="TOZO")

@app.get("/control/ping/")
async def ping() -> ResponseReturnValue:
    return {"ping" : "pong"}

quart_db = QuartDB(app)

@app.cli.command("recreate_db")
def recreate_db() -> None:
    db_url = urlparse(os.environ["TOZO_QUART_DB_DATABASE_URL"])
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"DROP DATABASE IF EXISTS {db_url.path.removeprefix('/')}"],
    )
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"DROP USER IF EXISTS {db_url.username}"],
    )
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB"],
       )
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"CREATE DATABASE {db_url.path.removeprefix('/')}"],
    )





