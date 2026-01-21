import os
from dotenv import load_dotenv
from veryfi import Client

load_dotenv()

veryfi_client = Client(
    client_id=os.getenv("VERYFI_CLIENT_ID"),
    client_secret=os.getenv("VERYFI_CLIENT_SECRET"),
    username=os.getenv("VERYFI_USERNAME"),
    api_key=os.getenv("VERYFI_API_KEY")
)
