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
    
    vendor_name = raw.get("vendor", {}).get("name")
    
    # Extract first line item name safely
    item_name = None
    if raw.get("line_items"):
        item_name = raw["line_items"][0].get("description")

    return {
        "customer_name": raw.get("bill_to", {}).get("name"),
        "vendor_name": vendor_name,
        "item_selling_name": item_name,
        "invoice_number": raw.get("invoice_number"),
        "invoice_date": raw.get("date"),
        "salesperson": raw.get("salesperson") or None,
    }

