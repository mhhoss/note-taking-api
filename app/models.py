import jdatetime
from pydantic import BaseModel, Field
import uuid


# مدلسازی داده ها 
class Note(BaseModel):
    id: str = Field(default_factory= lambda: str(uuid.uuid4()))
    name: str
    content: str | None = None
    created_at: str = Field(default_factory= lambda: jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M'))
    '''
    نوشتن اسم یادداشت برای ثبت شدن اجباریه ولی متن میتونه خالی باشه
    بصورت خودکار آیدی و تاریخ ثبت برای یادداشت ها ساخته میشه
    '''

class NoteCreate(BaseModel):
    name: str
    content: str | None = None


class NoteUpdate(BaseModel):
    name: str | None = None
    content: str | None = None


class NoteResponse(BaseModel):
    id: str
    name: str
    content: str | None = None
    created_at: str
