'''
مدیریت اتصال توابع به دیتابیس:

هر یادداشت: ...
    شامل اطلاعات آیدی، نام یادداشت، متن و تاریخ ساخت و یا ویرایش اون میشه
    با آیدی یکتا ساخته میشه و با همون آدرس پیدا میشه
    تاریخ بر اساس تاریخ جلالی ثبت میشه با موقعیت مکانی تهران/ایران
'''


import contextlib
import jdatetime
import sqlite3
from sqlite3 import Connection
from typing import Generator
import uuid
from app.models import Note
import logging


# ---------- پیکربندی ----------
DATABASE = 'notes.db'
logger = logging.getLogger(__name__)  # ثبت و مدیریت بهتر خطا ها در لاگر


# ---------- اتصال به دیتابیس ----------
@contextlib.contextmanager
def connect_to_db() -> Generator[Connection, None, None]:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # برای دسترسی به نام ستون و گرفتن خروجی دیکشنری
    try:
        yield conn
    finally:
        conn.close()


# ---------- row -> note ----------
def _row_to_note(row: sqlite3.Row) -> Note:
    '''
    این تابع داخلیه و برای تبدیل سطر ها به نت استفاده میشه
    تا از اضافه نویسی جلوگیری کنه و با صدا زدنش فرایند تبذیل رو انجام بده
    '''
    if row is None:
        return None
    note = dict(row)
    return Note(**note)


# ---------- ساخت جدول و شرط گذاری ----------
def init_db():
    create_table = """
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            content TEXT,
            created_at TEXT NOT NULL,
            is_edited INTEGER DEFAULT 0
        )"""

    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(create_table)  # کوئری ها اعمال میشه
        conn.commit()
    logger.info("جدول ساخته شد")


# -----// Database management using CRUD functions //-----

def create_note(name: str, content: str | None = None) -> Note: 
    note_id = str(uuid.uuid4())
    iran_now = jdatetime.datetime.now()
    created_at = iran_now.strftime("%Y/%m/%d %H:%M")

    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO notes (id, name, content, created_at, is_edited)
            VALUES (?, ?, ?, ?, ?)
            """,
            (note_id, name, content, created_at, 0),

        )
        conn.commit()
        # چون از context manager و دستور with استفاده کردم خودکار close() میشه

    return Note(id=note_id, name=name, content=content, created_at=created_at)
    # مقدار دهی میشه و خروجی برمیگرده


def get_all_notes() -> list[Note]:
    with connect_to_db() as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')  # از جدید به قدیم
        rows = cursor.fetchall()  # گرفتن همه ردیف ها

        return [Note(**dict(row)) for row in rows]


def get_note_by_id(note_id: str) -> Note | None:
    with connect_to_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()  # گرفتن ردیف مشخص بر اساس آیدی

        if row is None:
            return None

        return _row_to_note(row)


def update_note(note_id: str, name: str | None = None, content: str | None = None) -> Note | None:
    existing_note = get_note_by_id(note_id)  # نوت آیدی رو از دیتابیس میگیره برای آپدیت
    if existing_note is None:
        return None

    new_name = name if name is not None else existing_note.name
    new_content = content if content is not None else existing_note.content
    
    iran_now = jdatetime.datetime.now()
    new_datetime = iran_now.strftime("%Y/%m/%d %H:%M")

    with connect_to_db() as conn:
        cursor = conn.cursor()
    cursor.execute("""
        UPDATE notes
        SET name = ?, content = ?, created_at = ?, is_edited = ?
        WHERE id = ?
    """, (new_name, new_content, new_datetime, 1, note_id))
    conn.commit()

    return get_note_by_id(note_id)


def delete_note(note_id: str) -> bool:  # deleted successfully= True
    # اینجا خروجی صرفا مشخص میکنه که حذف موفق بوده یا نه و خروجی نت حذف شده رو نشون نمیده
    existing_note = get_note_by_id(note_id)
    if existing_note is None:
        return False
    
    with connect_to_db() as conn:
        cursor = conn.cursor()
    
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        changed = cursor.rowcount  # تعداد ردیف هایی ک در آخرین دستور تغییر کردن
        conn.commit()

        return changed > 0
        # اگر تغییرات برابر با صفر نباشه، عملیات حذف موفق بوده
