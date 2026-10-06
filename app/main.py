from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    description="REST API для керування завданнями",
    version="1.0.0"
)


class Task(BaseModel):
    id: int
    title: str
    completed: bool = False


tasks = [
    Task(id=1, title="Вивчити FastAPI", completed=False),
    Task(id=2, title="Зробити лабораторну роботу", completed=False)
]


@app.get("/api/tasks", response_model=list[Task])
def get_tasks():
    return tasks


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task with this ID already exists"
            )

    tasks.append(task)
    return task


@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(index)
            return {
                "message": "Task deleted",
                "task": deleted_task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )