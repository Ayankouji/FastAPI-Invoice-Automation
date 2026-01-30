import os
import json
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ======================================================
# GSTIN VALIDATION
# ======================================================
def is_valid_gstin(gstin):
    if not gstin:
        return False
    return bool(re.match(r"\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]", gstin))


# ======================================================
# EXTRACT GSTIN FROM OCR TEXT
# ======================================================
def extract_gstin_from_text(text):
    match = re.search(r"\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]", text)
    return match.group(0) if match else None


# ======================================================
# DETECT SUPPLIER COUNTRY FROM TEXT
# ======================================================
def detect_supplier_country(text):
    text = text.lower()

    if "united states" in text or "usa" in text or "california" in text:
        return "United States"
    if "india" in text:
        return "India"
    if "uk" in text or "united kingdom" in text:
        return "United Kingdom"

    return "Unknown"


# ======================================================
# AI EXPENSE CLASSIFICATION (GROQ)
# ======================================================
def ai_classify_expense(text):
    prompt = f"""
Return ONLY JSON:

{{
 "expense_account": "IT and Internet Expenses | Travel Expense | Office Supplies | Rent Expense | Other Expenses",
 "paid_through": "Bank | Cash | Petty Cash",
 "currency": "USD | INR | EUR"
}}

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)


# ======================================================
# FALLBACK RULE ENGINE
# ======================================================
def fallback_rules(text):
    text = text.lower()
    expense = "Other Expenses"
    paid = "Bank"
    currency = "INR"

    if "clerk" in text or "aws" in text or "cloud" in text:
        expense = "IT and Internet Expenses"
    if "travel" in text or "uber" in text:
        expense = "Travel Expense"
    if "office" in text:
        expense = "Office Supplies"
    if "$" in text or "usd" in text:
        currency = "USD"

    return {"expense_account": expense, "paid_through": paid, "currency": currency}


# ======================================================
# RCM DETECTION ENGINE (YOUR LOGIC)
# ======================================================
def detect_rcm(raw):
    text = raw.get("raw_text", "") or str(raw)

    # Try structured fields
    supplier_country = raw.get("vendor", {}).get("country")
    recipient_gstin = raw.get("bill_to", {}).get("gstin")

    # Fallback OCR extraction
    if not supplier_country:
        supplier_country = detect_supplier_country(text)

    if not recipient_gstin:
        recipient_gstin = extract_gstin_from_text(text)

    foreign_supplier = supplier_country not in ["India", "IN"]
    recipient_registered = is_valid_gstin(recipient_gstin)

    if foreign_supplier and recipient_registered:
        return {
            "rcm_applicable": True,
            "gst_type": "IGST",
            "gst_rate": 18,
            "supplier_country": supplier_country,
            "recipient_gstin": recipient_gstin
        }

    return {
        "rcm_applicable": False,
        "gst_type": None,
        "gst_rate": 0,
        "supplier_country": supplier_country,
        "recipient_gstin": recipient_gstin
    }


# ======================================================
# GST CALCULATION
# ======================================================
def calculate_gst(amount, rate):
    return round(amount * rate / 100, 2)


# ======================================================
# MAIN FUNCTION CALLED BY API
# ======================================================
def extract_expense_ai(raw):
    vendor = raw.get("vendor", {}).get("name")
    invoice_no = raw.get("invoice_number")
    date = raw.get("date")
    total = float(raw.get("total", 0))

    text = raw.get("raw_text", "") or str(raw)

    # AI classification with fallback
    try:
        ai = ai_classify_expense(text)
    except:
        ai = fallback_rules(text)

    # RCM detection
    rcm = detect_rcm(raw)

    gst_amount = 0
    if rcm["rcm_applicable"]:
        gst_amount = calculate_gst(total, rcm["gst_rate"])

    return {
        "vendor_name": vendor,
        "invoice_number": invoice_no,
        "invoice_date": str(date),
        "amount": total,

        "expense_account": ai["expense_account"],
        "paid_through": ai["paid_through"],
        "currency": ai["currency"],

        # GST / RCM OUTPUT
        "supplier_country": rcm["supplier_country"],
        "recipient_gstin": rcm["recipient_gstin"],
        "rcm_applicable": rcm["rcm_applicable"],
        "gst_type": rcm["gst_type"],
        "gst_rate": rcm["gst_rate"],
        "gst_amount": gst_amount
    }
