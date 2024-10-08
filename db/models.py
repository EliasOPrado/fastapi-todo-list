from .session import Base
from sqlalchemy import Column, Integer, String, Boolean, Integer, ForeignKey


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
