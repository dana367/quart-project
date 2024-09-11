from quart import Quart
from quart import ResponseReturnValue

app = Quart(__name__)

@app.get("/control/ping/")
async def ping() -> ResponseReturnValue:
    return {"ping" : "pong"}



