from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from my_app.routes.tasks import router as task_router


app = FastAPI(title="My Todo List")
app.mount("/static", StaticFiles(directory="static"))
app.include_router(task_router)
