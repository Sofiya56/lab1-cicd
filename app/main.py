from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TaskDb

app = FastAPI(title="Task API", description="REST API для керування завданнями", version="1.0.0")


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False


def get_or_404(db: Session, task_id: int) -> TaskDb:
    obj = db.get(TaskDb, task_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/tasks", response_model=List[Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(TaskDb).order_by(TaskDb.id)).all()


@app.post("/api/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task, db: Session = Depends(get_db)):
    obj = TaskDb(title=task.title, description=task.description, completed=task.completed)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, task_id)


@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    obj = get_or_404(db, task_id)
    obj.title, obj.description, obj.completed = task.title, task.description, task.completed
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db.delete(get_or_404(db, task_id))
    db.commit()
