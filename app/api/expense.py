from fastapi import APIRouter, UploadFile, File
import shutil, os

from app.services.veryfi_service import process_invoice
from app.utils.expense_ai import extract_expense_ai

router = APIRouter(prefix="/expense", tags=["Expense Automation"])

UPLOAD_DIR = "app/storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/extract")
async def extract_expense(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    raw_data = process_invoice(file_path)

    # AI + RCM
    result = extract_expense_ai(raw_data)

    # Cleanup
    os.remove(file_path)

    return result
