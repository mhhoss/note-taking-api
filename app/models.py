from typing import Optional
import jdatetime
from pydantic import BaseModel, Field
import uuid


# مدلسازی داده ها 
class Note(BaseModel):
    id: str = Field(default_factory= lambda: str(uuid.uuid4()))
    name: str
    content: Optional[str] = None
    created_at: str = Field(default_factory= lambda: jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M'))
    '''
    نوشتن اسم یادداشت برای ثبت شدن اجباریه ولی متن میتونه خالی باشه
    بصورت خودکار آیدی و تاریخ ثبت برای یادداشت ها ساخته میشه
    '''

class NoteCreate(BaseModel):
    name: str
    content: Optional[str] = None


class NoteUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(BaseModel):
    id: str
    title: str
    content: Optional[str] = None
    created_at: str
