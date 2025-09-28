'''
در این فایل منطق و توابع API نوشته شده
'''


import uuid
from fastapi import HTTPException
from typing import List, Optional

import jdatetime

from app.db import connect_to_db
from app.models import Note, NoteUpdate


# /Root
def root():
    return {"Message: API is running 🌪️"}


# ----------// CRUD functions //----------

def create_note(note: Note) -> Note:
    '''
    ذخیره نوت جدید با آیدی یکتا
    '''
    note_id = str(uuid.uuid4())
    iran_now = jdatetime.datetime.now()
    created_at = iran_now.strftime("%Y/%m/%d %H:%M")

    with connect_to_db() as conn:
        cursor = cursor.conn
        cursor.execute(
            """
            INSERT INTO notes (id, name, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (note_id, note.name, note.content, created_at)
        )
        conn.commit()

        
    return Note(id=note_id, name=note.name, content=note.content, created_at=created_at)


def get_all_notes() -> List[Note]:
    '''
    گرفتن کل نت ها به صورت لیست
    '''
    with connect_to_db() as conn:
        cursor = conn.cursor
        cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')
        rows = cursor.fetchall()

    return [Note(**dict(row)) for row in rows]


def get_note_by_id(note_id: str) -> Note:
    '''
    برگردوندن نوت براساس آیدی
    '''
    with connect_to_db() as conn:
        cursor = conn.cursor
        cursor.execute("SELECT * FROM notes WHERE id = ?")
        row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found!")
    
    return Note(**dict(row))


def update_note(note_id: str, updated_note: NoteUpdate) -> Note:
    '''
    بروز رسانی نت ها
    '''
    existing_note = get_note_by_id(note_id)
    if existing_note is None:
        raise HTTPException(status_code=404, detail=f"note {note_id}, not found!")
    
    with connect_to_db() as conn:
        cursor = conn.cursor
        cursor.execute(
            """
            UPDATE notes
            SET name = ?, content = ?, updated_at = ?
            WHERE id = ?
            """,
            (updated_note.name, updated_note.content)
        )
        conn.commit()

    return get_note_by_id(note_id)


def delete_note(note_id: str) -> Optional[Note]:
    '''
    حذف نت با آیدی یکتا
    در صورت نبودن نت، None رو برمیگردونه
    '''
    existing_note = get_note_by_id(note_id)
    if existing_note is None:
        return None
    
    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()

    return existing_note
