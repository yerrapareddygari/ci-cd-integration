from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


todos: Dict[int, Todo] = {}
next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos", response_model=List[Todo])
def list_todos():
    return list(todos.values())


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate):
    global next_id
    todo = Todo(id=next_id, title=payload.title)
    todos[next_id] = todo
    next_id += 1
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate):
    todo = todos.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if payload.title is not None:
        todo.title = payload.title
    if payload.completed is not None:
        todo.completed = payload.completed
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
