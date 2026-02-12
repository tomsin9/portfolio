from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime, timezone

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    excerpt: Optional[str] = None
    content: str
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    is_published: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()"}
        )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()"}
        )