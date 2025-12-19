import re

def extract_amount(text: str) -> float | None:
    matches = re.findall(r"R?\$?\s?(\d+[.,]\d{2})", text)

    if not matches:
        return None

    normalized = []
    for value in matches:
        clean_val = value.replace("R$", "").strip()
        clean_val = clean_val.replace(".", "").replace(",", ".")
        try:
            normalized.append(float(clean_val))
        except ValueError:
            continue

    return max(normalized) if normalized else None

def extract_currency(text: str) -> str:
    text_lower = text.lower()
    if "r$" in text_lower or "brl" in text_lower or "reais" in text_lower:
        return "R$"
    if "€" in text_lower or "eur" in text_lower:
        return "€"
    if "£" in text_lower:
        return "£"
    return "$" 

def map_month_name_to_number(month_name: str) -> str:
    months = {
        "janeiro": "01", "fevereiro": "02", "março": "03", "marco": "03",
        "abril": "04", "maio": "05", "junho": "06",
        "julho": "07", "agosto": "08", "setembro": "09",
        "outubro": "10", "novembro": "11", "dezembro": "12"
    }
    return months.get(month_name.lower(), "01")

def extract_date(text: str) -> str | None:
    text_lower = text.lower()
    
    match_extenso = re.search(r"(\d{1,2})\s+de\s+([a-zç]+)\s+de\s+(\d{4})", text_lower)
    
    if match_extenso:
        day = match_extenso.group(1).zfill(2) 
        month = map_month_name_to_number(match_extenso.group(2))
        year = match_extenso.group(3)
        return f"{year}-{month}-{day}" 
    match_num = re.search(r"(\d{2})[/-](\d{2})[/-](\d{4})", text)
    if match_num:
        return f"{match_num.group(3)}-{match_num.group(2)}-{match_num.group(1)}"

    return "Unknown Date"

def extract_vendor(text: str) -> str:
    text_lower = text.lower()
    
    known_vendors = {
        "apple": "Apple Services",
        "icloud": "Apple Services",
        "uber": "Uber",
        "99": "99 App",
        "amazon": "Amazon",
        "starbucks": "Starbucks",
        "mcdonalds": "McDonald's",
        "bk": "Burger King",
        "gol": "GOL Linhas Aéreas",
        "latam": "Latam Airlines"
    }
    
    for key, formal_name in known_vendors.items():
        if key in text_lower:
            return formal_name
            
    match_conta = re.search(r"conta\s+([a-zA-Z0-9]+):", text_lower)
    if match_conta:
        return match_conta.group(1).capitalize()

    return "Unknown Vendor"

def infer_category(text: str) -> str:
    text_lower = text.lower()

    categories = {
        "Meal": ["meal", "food", "restaurant", "lunch", "restaurante", "ifood", "burger", "coffee"],
        "Hotel": ["hotel", "inn", "room", "hospedagem", "airbnb"],
        "Transport": ["uber", "99", "taxi", "cab", "transport", "viagem"],
        "Software": ["icloud", "apple", "google", "aws", "microsoft", "adobe", "saas", "assinatura"]
    }

    for category, keywords in categories.items():
        if any(key in text_lower for key in keywords):
            return category

    return "Other"

def normalize_receipt(text: str) -> dict:
    return {
        "amount": extract_amount(text),
        "currency": extract_currency(text),
        "category": infer_category(text),
        "date": extract_date(text),
        "vendor": extract_vendor(text),
        "receipt_provided": bool(text.strip())
    }