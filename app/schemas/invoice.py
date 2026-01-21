# from pydantic import BaseModel
# from typing import List, Optional

# class LineItem(BaseModel):
#     description: Optional[str]
#     quantity: Optional[float]
#     rate: Optional[float]
#     amount: Optional[float]

# class InvoiceResponse(BaseModel):
#     vendor_name: Optional[str]
#     invoice_number: Optional[str]
#     invoice_date: Optional[str]
#     currency: Optional[str]
#     subtotal: float
#     tax: float | None = 0.0
#     total: float
#     line_items: List[LineItem]


from pydantic import BaseModel
from typing import Optional

class InvoiceMinimalResponse(BaseModel):
    customer_name: Optional[str]
    invoice_number: Optional[str]
    invoice_date: Optional[str]
    salesperson: Optional[str]
 
