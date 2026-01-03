"""fastapi todo app - rest api for todo operations

this module implements the main fastapi application with rest endpoints
for all todo operations (crud).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
from src.store import TaskStore
from src.models import Task

# initialize fastapi app
app = FastAPI(
    title="todo app api",
    description="rest api for in-memory todo application",
    version="1.0.0"
)

# enable cors for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# global task store (in-memory)
store = TaskStore()

# pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: str = ""

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class TaskResponse(BaseModel):
    id: int | None
    title: str
    description: str
    completed: bool
    created_at: datetime
    completed_at: datetime | None

# serve static files from public directory
public_dir = Path(__file__).parent.parent / "public"
if public_dir.exists():
    app.mount("/static", StaticFiles(directory=public_dir), name="static")

# root endpoint - serve index.html
@app.get("/", response_class=FileResponse)
async def root():
    """serve the web ui"""
    index_file = public_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"error": "index.html not found"}

# root endpoint for api info
@app.get("/api")
def api_info():
    """api info"""
    return {
        "name": "todo app api",
        "version": "1.0.0",
        "endpoints": {
            "get /tasks": "list all tasks",
            "post /tasks": "create a new task",
            "get /tasks/{task_id}": "get task details",
            "put /tasks/{task_id}": "update task",
            "delete /tasks/{task_id}": "delete task",
        }
    }

# list all tasks
@app.get("/tasks")
def list_tasks(filter: str = "all"):
    """list all tasks with optional filtering"""
    try:
        tasks = store.list(filter=filter)
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                completed_at=task.completed_at,
            )
            for task in tasks
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# create a new task
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    """create a new task"""
    try:
        created = store.add(task.title, task.description)
        return TaskResponse(
            id=created.id,
            title=created.title,
            description=created.description,
            completed=created.completed,
            created_at=created.created_at,
            completed_at=created.completed_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# get task details
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """get details of a specific task"""
    task = store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task not found (id: {task_id})")
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        completed_at=task.completed_at,
    )

# update task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """update a task"""
    try:
        changes = {}
        if task_update.title is not None:
            changes["title"] = task_update.title
        if task_update.description is not None:
            changes["description"] = task_update.description
        if task_update.completed is not None:
            changes["completed"] = task_update.completed
        
        updated = store.update(task_id, **changes)
        return TaskResponse(
            id=updated.id,
            title=updated.title,
            description=updated.description,
            completed=updated.completed,
            created_at=updated.created_at,
            completed_at=updated.completed_at,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"task not found (id: {task_id})")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """delete a task"""
    result = store.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"task not found (id: {task_id})")
    
    return {"message": f"task {task_id} deleted"}

# health check
@app.get("/health")
def health_check():
    """health check endpoint"""
    return {"status": "healthy"}

# list all tasks
@app.get("/tasks")
def list_tasks(filter: str = "all"):
    """list all tasks with optional filtering"""
    try:
        tasks = store.list(filter=filter)
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                completed_at=task.completed_at,
            )
            for task in tasks
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# create a new task
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    """create a new task"""
    try:
        created = store.add(task.title, task.description)
        return TaskResponse(
            id=created.id,
            title=created.title,
            description=created.description,
            completed=created.completed,
            created_at=created.created_at,
            completed_at=created.completed_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# get task details
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """get details of a specific task"""
    task = store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task not found (id: {task_id})")
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        completed_at=task.completed_at,
    )

# update task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """update a task"""
    try:
        changes = {}
        if task_update.title is not None:
            changes["title"] = task_update.title
        if task_update.description is not None:
            changes["description"] = task_update.description
        if task_update.completed is not None:
            changes["completed"] = task_update.completed
        
        updated = store.update(task_id, **changes)
        return TaskResponse(
            id=updated.id,
            title=updated.title,
            description=updated.description,
            completed=updated.completed,
            created_at=updated.created_at,
            completed_at=updated.completed_at,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"task not found (id: {task_id})")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """delete a task"""
    result = store.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"task not found (id: {task_id})")
    
    return {"message": f"task {task_id} deleted"}

# health check
@app.get("/health")
def health_check():
    """health check endpoint"""
    return {"status": "healthy"}
