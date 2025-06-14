import json
import os
from datetime import datetime

DATA_FILE = "call_data.json"

def save_call_data(phone_number, transcript, ai_response, summary):
    """
    Saves call info to a local JSON file.
    """
    call_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "phone_number": phone_number,
        "transcript": transcript,
        "ai_response": ai_response,
        "summary": summary,
    }

    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass

    data.append(call_record)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[DB] Saved call data for {phone_number}")

def save_lead_data(lead_info):
    """
    Saves a new lead to a separate JSON file.
    """
    LEAD_FILE = "leads.json"

    lead_info["timestamp"] = datetime.utcnow().isoformat()

    data = []
    if os.path.exists(LEAD_FILE):
        with open(LEAD_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass

    data.append(lead_info)

    with open(LEAD_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[DB] Saved lead data: {lead_info.get('name', 'Unnamed')}")
