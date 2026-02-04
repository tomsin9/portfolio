from sqlmodel import SQLModel, Field
from typing import Optional

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    is_published: bool = Field(default=False)