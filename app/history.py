import json
import os
import uuid
from datetime import datetime

HISTORY_FILE = "history.json"

class HistoryManager:
    def __init__(self):
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as f:
                json.dump([], f)

    def add_entry(self, filename, decision, receipt_data):
        entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename,
            "vendor": receipt_data.get("vendor", "Unknown"),
            "amount": f"{receipt_data.get('currency', '$')} {receipt_data.get('amount')}",
            "status": "APPROVED" if decision["approved"] else "REJECTED",
            "reason": decision["reason"]
        }

        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
        
        data.insert(0, entry)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(data, f, indent=4)
            
        return entry

    def get_all(self):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)