import fastapi

from src.internal.domain.structures.adapter.transport.ws.broadcasters.task import ITaskBroadcaster
from .base import AnonymousBroadcaster


class TaskBroadcaster(ITaskBroadcaster, AnonymousBroadcaster):
    async def handle(self, socket: fastapi.WebSocket):
        await socket.accept()
        try:
            await self.connect(socket)
            while True:
                await socket.receive_text()
        except fastapi.WebSocketDisconnect:
            await self.disconnect(socket)
