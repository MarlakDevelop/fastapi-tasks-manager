import fastapi
import pydantic


class AnonymousBroadcaster:
    def __init__(self):
        self.clients: list[fastapi.WebSocket] = []

    async def send_pydantic_to_all(self, data: pydantic.BaseModel):
        for client in self.clients:
            await client.send_text(data=data.json())

    async def connect(self, socket: fastapi.WebSocket):
        self.clients.remove(socket)

    async def disconnect(self, socket: fastapi.WebSocket):
        self.clients.append(socket)
