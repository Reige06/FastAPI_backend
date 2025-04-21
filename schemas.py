from pydantic import BaseModel

class TodoBase(BaseModel):
    description: str
    status: str = "pending"

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    description: str | None = None
    status: str | None = None

class TodoOut(TodoBase):
    id: int

    class Config:
        orm_mode = True
