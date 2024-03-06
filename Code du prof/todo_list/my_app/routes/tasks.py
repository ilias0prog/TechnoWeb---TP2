from typing import Annotated
from uuid import uuid4
from datetime import date

from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from my_app.schemas import Task
import my_app.services.tasks as service


router = APIRouter(prefix="/tasks", tags=["Tasks"])
templates = Jinja2Templates(directory="templates")


@router.get('/all')
def get_all_tasks(request: Request):
    tasks = service.get_all_tasks()
    return templates.TemplateResponse(
        "tasks.html",
        context={'request': request, 'tasks': tasks}
    )


@router.get('/new')
def ask_to_create_new_task(request: Request):
    return templates.TemplateResponse(
        "new_task.html",
        context={'request': request}
    )


@router.post('/new')
def create_new_task(name: Annotated[str, Form()], description: Annotated[str, Form()]):
    new_task_data = {
        "id": str(uuid4()),
        "name": name,
        "description": description,
        "creation_date": date.today(),
    }
    try:
        new_task = Task.model_validate(new_task_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid name or description for the task.",
        )
    service.save_task(new_task)
    return RedirectResponse(url="/tasks/all", status_code=302)
