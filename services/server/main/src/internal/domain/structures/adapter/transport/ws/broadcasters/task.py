import fastapi
import pydantic


class ITaskBroadcaster:
    async def handle(self, socket: fastapi.WebSocket):
        pass

    async def send_pydantic_to_all(self, data: pydantic.BaseModel):
        pass
