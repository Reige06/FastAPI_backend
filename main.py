from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fetch all todos
@app.get("/api/todos/", response_model=list[schemas.TodoOut])
def read_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

# Create a new todo
@app.post("/api/todos/", response_model=schemas.TodoOut)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Update a todo
@app.put("/api/todos/{todo_id}/", response_model=schemas.TodoOut)
def update_todo(todo_id: int, update_data: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if update_data.description is not None:
        todo.description = update_data.description
    if update_data.status is not None:
        todo.status = update_data.status

    db.commit()
    db.refresh(todo)
    return todo

# Delete a todo
@app.delete("/api/todos/{todo_id}/")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
