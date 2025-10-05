from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas import NoteCreate, NoteUpdate, NoteResponse
from app.models import Note
from app.crud import create_note, get_all_notes, get_note_by_id, update_note, delete_note


router = APIRouter(
    prefix="/notes",  # مسیر اصلی نوت ها بصورت پیش فرض
    tags=["Notes"]
)


# ---------- endpoints ----------

@router.post("/", response_model= NoteResponse, summary= "نوشتن یادداشت...")
def create_new_note(note: NoteCreate):
    '''
    ذخیره نوت جدید با آیدی یکتا
    '''
    return create_note(note)


@router.get("/", response_model= List[Note], summary= "دریافت لیست یادداشت ها")
def get_all_router_notes():
    '''
    گرفتن کل نت ها به صورت لیست
    '''
    return get_all_notes()


@router.get("/{note_id}", response_model=Note, summary= "دریافت یادداشت با شناسه")
def get_router_note_by_id(note_id: str):
    '''
    برگردوندن نوت براساس آیدی
    '''
    note = get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id}, not found!")
    return note


@router.put("/{note_id}", response_model=Note, summary= "به روزرسانی یادداشت")
def update_router_note(note_id: str, updated_note: NoteUpdate):
    '''
    بروز رسانی نت ها
    '''
    note = update_note(note_id, updated_note)
    if not note:
        raise HTTPException(status_code=404, detail=f"note {note_id}, not found!")
    return note


@router.delete("/{note_id}", response_model=Note, summary= "حذف یادداشت")
def delete_router_note(note_id: str):
    '''
    حذف نت با آیدی یکتا
    '''
    note = delete_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="یادداشت پیدا نشد!")
    return note
