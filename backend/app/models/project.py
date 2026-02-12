from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime, timezone

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str = "Web"
    image: Optional[str] = None
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    order: str = "0"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()"})
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()"})