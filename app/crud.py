from datetime import datetime
import uuid
from fastapi import FastAPI, HTTPException
from typing import List

from models import Note, NoteUpdate


app = FastAPI(
    title= "Note Taking API",
    description= "This is a simple RESTful API service to taking note"
)


notes_db = []


@app.get("/")
def root():
    return {"Message: API is running 🌪️"}


@app.post("/notes/", response_model= Note)
def create_note(note: Note):
    '''
    ذخیره نوت جدید با آیدی یکتا
    '''
    note.id = str(uuid.uuid4())
    note.created_at = datetime.now()
    notes_db.append(note)
    return note


@app.get("/notes", response_model= List[Note])
def list_notes():
    '''
    گرفتن کل نت ها به صورت لیست
    '''
    return notes_db


@app.get("/notes/{note_id}", response_model=Note)
def get_note_by_id(note_id: str):
    '''
    برگردوندن نوت براساس آیدی
    '''
    found_note = next((note for note in notes_db if note.id == note_id), None)
    if found_note:
        return found_note
    raise HTTPException(status_code=404, detail=f"Note {note_id}, not found!")


@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, updated_note: NoteUpdate):
    '''
    بروز رسانی نت ها
    '''
    found_note = next((note for note in notes_db if note.id == note_id), None)
    if found_note:
        found_note.title = updated_note.title
        found_note.content = updated_note.content
        return found_note
    raise HTTPException(status_code=404, detail=f"note {note_id}, not found!")


@app.delete("/notes/{note_id}", response_model=Note)
def delete_note(note_id: str):
    '''
    حذف نت با آیدی یکتا
    '''
    found_note = next((note for note in notes_db if note_id == note.id), None)
    if found_note:
        notes_db.remove(found_note)
        return found_note
    raise HTTPException(status_code=404, detail="Note not found!")