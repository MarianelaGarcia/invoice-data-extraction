import pdfplumber
import pandas as pd
import os
import re
import pytesseract
import logging
import json
from PIL import Image

# =========================
# LOGGING PROFESIONAL
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# OCR
# =========================

def ocr_page(page):
    image = page.to_image(resolution=300).original
    return pytesseract.image_to_string(image)


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"
            else:
                text += ocr_page(page)

    return text


# =========================
# NORMALIZACIÓN
# =========================

def normalize_amount(amount):
    if not amount:
        return None
    amount = amount.replace(",", ".")
    amount = re.sub(r"[^\d.]", "", amount)
    try:
        return float(amount)
    except:
        return None


# =========================
# MULTI-IDIOMA
# =========================

INVOICE_PATTERNS = [
    r'INVOICE\s*NO[:\s]*([A-Z0-9\-]+)',
    r'INVOICE\s*#[:\s]*([A-Z0-9\-]+)',
    r'INVOICE\s*NUMBER[:\s]*([A-Z0-9\-]+)',
    r'FACTURA[:\s]*([A-Z0-9\-]+)',
    r'RECHNUNG[:\s]*([A-Z0-9\-]+)'
]

TOTAL_KEYWORDS = [
    "total", "grand total", "amount due",
    "importe total", "gesamt", "totale"
]


# =========================
# HELPERS
# =========================

def extract_invoice(line):
    for pattern in INVOICE_PATTERNS:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_currency_and_amount(line):
    match = re.search(r'([€$£])\s*([\d.,]+)', line)
    if match:
        return match.group(1), match.group(2)
    return None, None


# =========================
# MAIN PARSER
# =========================

def extract_data(text):
    data = {
        "invoice": None,
        "total": None,
        "currency": None
    }

    for line in text.split("\n"):
        line_clean = line.strip().lower()

        # -------- INVOICE --------
        if not data["invoice"]:
            inv = extract_invoice(line_clean)
            if inv:
                data["invoice"] = inv

        # -------- TOTAL --------
        if any(k in line_clean for k in TOTAL_KEYWORDS):
            if "subtotal" in line_clean:
                continue

            currency, amount = extract_currency_and_amount(line_clean)

            if amount:
                data["total"] = normalize_amount(amount)

            if currency:
                data["currency"] = currency

    return data


# =========================
# MAIN PIPELINE
# =========================

folder = "invoices"
results = []

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        try:
            path = os.path.join(folder, file)

            logging.info(f"Processing {file}")

            text = extract_text(path)
            data = extract_data(text)

            # -------- DEBUG --------
            print("\n====================")
            print(f"FILE: {file}")
            print("TEXT PREVIEW:")
            print(text[:300])
            print("EXTRACTED DATA:")
            print(data)

            data["file"] = file
            results.append(data)

        except Exception as e:
            logging.error(f"Error with {file}: {e}")


# =========================
# OUTPUT
# =========================

os.makedirs("output", exist_ok=True)

df = pd.DataFrame(results).fillna("")

# Excel
excel_path = "output/output.xlsx"
df.to_excel(excel_path, index=False)

# CSV
csv_path = "output/output.csv"
df.to_csv(csv_path, index=False)

# JSON
json_path = "output/output.json"
with open(json_path, "w") as f:
    json.dump(results, f, indent=2)

logging.info("All files generated successfully ")
