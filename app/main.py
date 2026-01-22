# from fastapi import FastAPI, UploadFile, File
# import shutil
# import os

# from app.services.veryfi_service import process_invoice
# from app.utils.cleaner import clean_invoice_data
# from app.schemas.invoice import InvoiceResponse

# app = FastAPI(title="Invoice OCR Automation API")

# UPLOAD_DIR = "app/storage/uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/extract-invoice", response_model=InvoiceResponse)
# async def extract_invoice(file: UploadFile = File(...)):
#     file_path = f"{UPLOAD_DIR}/{file.filename}"

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     raw_data = process_invoice(file_path)
#     clean_data = clean_invoice_data(raw_data)

#     return clean_data
from fastapi import FastAPI, UploadFile, File
import shutil
import os

from app.services.veryfi_service import process_invoice
from app.utils.cleaner import extract_invoice_minimal
from app.schemas.invoice import InvoiceMinimalResponse

app = FastAPI(title="Invoice OCR Minimal API")

UPLOAD_DIR = "app/storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Render health check
@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/extract-invoice", response_model=InvoiceMinimalResponse)
async def extract_invoice(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_data = process_invoice(file_path)

    # delete file after processing
    os.remove(file_path)

    return extract_invoice_minimal(raw_data)
