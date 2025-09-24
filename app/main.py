from datetime import datetime
from fastapi import FastAPI, HTTPException

from models import Note

app = FastAPI()

notes_db = []


@app.get("/")
def root():
    return {"message: API is running..."}


@app.post("/notes/", response_model= Note)  # ذخیره نوت جدید
def create_items(note: Note):
    note.created_at = datetime.now()
    note.updated_at = note.created_at
    notes_db.append(note)
    return note


@app.get(response_model= list[Note])
def list_notes():
    return notes_db


@app.get("/items/{note_id}", response_model=Note)  # برگردوندن نوت براساس اندیس
def get_note_by_id(note_id: int) -> str:
    if 0 <= note_id <= len(notes_db):
        return notes_db[note_id]
    else:
        raise HTTPException(stats_code=404, detail=f"note {note_id}, not found!")


@app.put("/items/{note_id}", response_model=Note)
def update_note(note_id: int, updated_note: None):
    if 0 <= note_id <= len(notes_db):
        notes_db[note_id].title = updated_note.title
        notes_db[note_id].content = updated_note.content
        notes_db[note_id].updated_at = datetime.now()
        return notes_db[note_id]
    raise HTTPException(stats_code=404, detail=f"note {note_id}, not found!")


@app.delete("/notes/{note_id}", response_model=Note)
def delete_note(note_id: int):
    if 0 <= note_id <= len(notes_db):
        notes_db.pop(note_id)
        return {f"{note_id}, deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found!")