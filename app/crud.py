'''
در این فایل منطق و توابع API نوشته شده
'''


import uuid
from fastapi import HTTPException
from typing import List

import jdatetime

from app.db import connect_to_db
from app.schemas import NoteCreate, NoteUpdate, NoteResponse
from app.models import Note


# ----- برای مشخص کردن فرم نمایش نهایی با برچسب مناسب برای تاریخ -----
def format_note_response(note: Note) -> NoteResponse:
    label = "Edited at:" if note.is_edited else "Created at:"
    timestamp = f"{label} {note.created_at}"
    return NoteResponse(
        id=note.id,
        name=note.name,
        content=note.content,
        timestamp=timestamp
    )


# ----------// CRUD functions //----------

def create_note(note: NoteCreate) -> NoteResponse:
    '''
    ذخیره نوت جدید با آیدی یکتا
    '''
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
            (note_id, note.name, note.content, created_at, 0)
        )
        conn.commit()

        
    new_note = Note(id=note_id, name=note.name, content=note.content, created_at=created_at, is_edited=0)
    return format_note_response(new_note)

def get_all_notes() -> List[NoteResponse]:
    '''
    گرفتن کل نت ها به صورت لیست
    '''
    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')
        rows = cursor.fetchall()

    notes = [Note(**dict(row)) for row in rows]
    return [format_note_response(note) for note in notes]


def get_note_by_id(note_id: str) -> Note:
    '''
    برگردوندن نوت براساس آیدی
    '''
    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found!")
    
    return Note(**dict(row))


def update_note(note_id: str, updated_note: NoteUpdate) -> NoteResponse:
    '''
    بروز رسانی نت ها
    '''
    existing_note = get_note_by_id(note_id)
    if existing_note is None:
        raise HTTPException(status_code=404, detail=f"note {note_id}, not found!")
    
    new_name = updated_note.name if updated_note.name is not None else existing_note
    new_content = updated_note.content if updated_note.content is not None else existing_note
    iran_now = jdatetime.datetime.now()
    new_datetime = iran_now.strftime("%Y/%m/%d %H:%M")

    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE notes
            SET name = ?, content = ?, created_at = ?, is_edited = ?
            WHERE id = ?
            """,
            (
                new_name,
                new_content,
                new_datetime,
                1,
                note_id
            )
        )
        conn.commit()

    updated_note_row = get_note_by_id(note_id)
    return format_note_response(updated_note_row)


def delete_note(note_id: str) -> Note | None:
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
