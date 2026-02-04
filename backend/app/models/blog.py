from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    date: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = Field(default=False)