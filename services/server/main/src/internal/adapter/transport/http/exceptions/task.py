import fastapi


TaskNotFoundException = fastapi.HTTPException(status_code=404, detail='Task not found')
