from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid


# مدلسازی داده ها
class Note(BaseModel):
    id: str
    name: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
            '''
            اگر آیدی مشخص نشده باشه اینجا ایجاد و مدلسازی میشه
            '''
