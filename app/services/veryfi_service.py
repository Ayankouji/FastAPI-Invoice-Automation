from app.config import veryfi_client

def process_invoice(file_path: str):
    return veryfi_client.process_document(
        file_path=file_path,
        categories=["Invoice"]
    )
