import jdatetime
from pydantic import BaseModel, Field
import uuid


# مدلسازی داده ها 
class Note(BaseModel):
    id: str = Field(default_factory= lambda: str(uuid.uuid4()))
    name: str
    content: str | None = None
    created_at: str = Field(
        default_factory= lambda: jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M')
        )
    is_edited: int = 0
    '''
    نوشتن اسم یادداشت برای ثبت شدن اجباریه ولی متن میتونه خالی باشه
    بصورت خودکار آیدی و تاریخ ثبت برای یادداشت ها ساخته میشه
    
    ->  همچنین یک فیلد تاریخ وجود داره که همیشه آخرین زمان تغییر رو نشون میده
        و بسته به اینکه یادداشت تازه ساخته شده یا ویرایش شده، در خروجی نمایش
        created_at / edited_at
        0 = تازه ساخته شده
        1 = ویرایش شده
    '''
