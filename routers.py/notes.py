from ast import List
from fastapi import APIRouter, HTTPException
from app.models import Note, NoteUpdate
from app.crud import create_note, get_all_notes, get_note_by_id, update_note, delete_note


router = APIRouter(
    prefix="/notes",  # مسیر اصلی برای نوت‌ها
    tags=["Notes"]
)


# ---------- endpoints ----------

@router.post("/notes/", response_model= Note, summary= "نوشتن یادداشت...")
def create_note(note: Note):
    '''
    ذخیره نوت جدید با آیدی یکتا
    '''
    return create_note(note)


@router.get("/notes", response_model= List[Note], sammary= "دریافت لیست یادداشت ها")
def get_all_notes():
    '''
    گرفتن کل نت ها به صورت لیست
    '''
    return get_all_notes()


@router.get("/notes/{note_id}", response_model=Note, sammary= "دریافت یادداشت با شناسه")
def get_note_by_id(note_id: str):
    '''
    برگردوندن نوت براساس آیدی
    '''
    note = get_note_by_id()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id}, not found!")
    return note


@router.put("/notes/{note_id}", response_model=Note, sammary= "به روزرسانی یادداشت")
def update_note(note_id: str, updated_note: NoteUpdate):
    '''
    بروز رسانی نت ها
    '''
    note = update_note(note_id, updated_note)
    if not note:
        raise HTTPException(status_code=404, detail=f"note {note_id}, not found!")
    return note


@router.delete("/notes/{note_id}", response_model=Note, sammary= "حذف یادداشت")
def delete_note(note_id: str):
    '''
    حذف نت با آیدی یکتا
    '''
    note = delete_note()
    if not note:
        raise HTTPException(status_code=404, detail="یادداشت پیدا نشد!")
    return note
