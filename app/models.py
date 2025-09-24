from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Note(BaseModel):
    name: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    topic: str

