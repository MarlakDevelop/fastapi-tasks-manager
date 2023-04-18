import fastapi

from src.internal.adapter.data.repositories.task import TaskRepository
from src.internal.adapter.transport.http.controllers.task import TaskController
from src.internal.adapter.transport.ws.broadcasters.task import TaskBroadcaster
from src.internal.domain.models.base import Base
from src.internal.infrastructure.database import init_database, get_db_session
from src.internal.infrastructure.router.task import TaskRouter
from src.internal.usecase.services.task import TaskService


app = fastapi.FastAPI()

task_repository = TaskRepository(get_db_session=get_db_session)

task_service = TaskService(task_repository=task_repository)

task_broadcaster = TaskBroadcaster()
task_controller = TaskController(task_service=task_service, task_broadcaster=task_broadcaster)

task_router = TaskRouter(app=app, task_controller=task_controller, task_broadcaster=task_broadcaster)
app = task_router.get_app()


@app.on_event("startup")
async def startup():
    await init_database(base=Base)


@app.on_event("shutdown")
async def shutdown():
    pass
