from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone

class ProjectRead(BaseModel):
    id: int
    title: str
    description: str
    category: str
    image: Optional[str] = None
    tags: List[str]
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    order: str

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.astimezone(timezone.utc).isoformat()
        }
    )