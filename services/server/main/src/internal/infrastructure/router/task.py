import fastapi

from src.internal.domain.structures.adapter.transport.http.controllers.task import ITaskController
from src.internal.domain.structures.adapter.transport.ws.broadcasters.task import ITaskBroadcaster


class TaskRouter:
    def __init__(
        self,
        app: fastapi.FastAPI,
        task_controller: ITaskController,
        task_broadcaster: ITaskBroadcaster,
        api_prefix: str = '/api/v1/tasks',
        channels_prefix: str = '/channels/v1/tasks'
    ):
        self.app = app
        self.api_prefix = api_prefix
        self.channels_prefix = channels_prefix
        self._add_api_routes(task_controller=task_controller)
        self._add_channels_routes(task_broadcaster=task_broadcaster)

    def get_app(self) -> fastapi.FastAPI:
        return self.app

    def _add_api_routes(
        self,
        task_controller: ITaskController
    ):
        router = fastapi.APIRouter(prefix=self.api_prefix, tags=['Tasks'])
        router.get('/')(task_controller.get)
        router.post('/')(task_controller.post)
        router.patch('/')(task_controller.patch)
        router.delete('/')(task_controller.delete)
        router.post('/one')(task_controller.post_one)
        router.get('/{taskId}')(task_controller.get_one)
        router.patch('/{taskId}')(task_controller.patch_one)
        router.delete('/{taskId}')(task_controller.delete_one)
        self.app.include_router(router)

    def _add_channels_routes(
        self,
        task_broadcaster: ITaskBroadcaster
    ):
        self.app.websocket(self.channels_prefix)(task_broadcaster.handle)
