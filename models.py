from sqlalchemy import Column, Integer, String
from database import Base

class Todo(Base):
    __tablename__ = "Reige_todo"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default="pending")