'''
در این فایل ساختار داده هایی که از کاربر گرفته میشود
و داده هایی که به کاربر نمایش داده میشود تعریف شده است

*این قسمت مستقل از دیتابیس هست و با API تعامل دارد
برخلاف فایل models که فرایند ذخیره دیتا در دیتابیس را برعهده دارد
'''


from pydantic import BaseModel


# وقتی کاربر نوت جدید می‌سازه
class NoteCreate(BaseModel):
    name: str
    content: str | None = None

# وقتی کاربر نوت رو آپدیت می‌کنه
class NoteUpdate(BaseModel):
    name: str | None = None
    content: str | None = None

# وقتی نوت رو به کاربر برمیگردونیم
class NoteResponse(BaseModel):
    id: str
    name: str
    content: str | None = None
    created_at: str
    # وقتی اطلاعات به این کلاس وارد میشود خروجی بصورت JSON خواهد بود
