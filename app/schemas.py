'''
در این فایل ساختار داده هایی که از کاربر گرفته میشود
و داده هایی که به کاربر نمایش داده میشوند تعریف میشود
ورودی ها <-
خروجی ها ->

*این قسمت مستقل از دیتابیس هست و با API تعامل داره
برخلاف فایل models که مستقیما با دیتابیس در تعامله
'''


from pydantic import BaseModel


# وقتی کاربر نوت جدید می‌سازه
class NoteCreate(BaseModel):
    name: str
    content: str | None

# وقتی کاربر نوت رو آپدیت می‌کنه
class NoteUpdate(BaseModel):
    name: str | None
    content: str | None

# وقتی نوت رو به کاربر برمیگردونیم
class NoteResponse(BaseModel):
    id: str
    name: str
    content: str | None
    created_at: str
    # وقتی اطلاعات به این کلاس وارد میشود خروجی بصورت JSON خواهد بود
