# def clean_invoice_data(raw):
#     return {
#         "vendor_name": raw.get("vendor", {}).get("name"),
#         "invoice_number": raw.get("invoice_number"),
#         "invoice_date": raw.get("date"),
#         "currency": raw.get("currency"),
#         "subtotal": raw.get("subtotal", 0),
#         "tax": raw.get("tax", 0),
#         "total": raw.get("total", 0),
#         "line_items": [
#             {
#                 "description": item.get("description"),
#                 "quantity": item.get("quantity", 1),
#                 "rate": item.get("price"),
#                 "amount": item.get("total")
#             }
#             for item in raw.get("line_items", [])
#         ]
#     }

def extract_invoice_minimal(raw):
    return {
        "customer_name": (
            raw.get("bill_to", {}).get("name")
            or raw.get("vendor", {}).get("name")
        ),
        "invoice_number": raw.get("invoice_number"),
        "invoice_date": raw.get("date"),
        "salesperson": raw.get("salesperson") or None
    }
