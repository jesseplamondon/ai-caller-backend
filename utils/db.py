import json
import os
from datetime import datetime
import asyncio

DATA_FILE = "call_data.json"
LEAD_FILE = "leads.json"

# Async wrappers for file IO
async def save_call_data(phone_number, transcript, ai_response, summary):
    call_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "phone_number": phone_number,
        "transcript": transcript,
        "ai_response": ai_response,
        "summary": summary,
    }

    data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append(call_record)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[DB] Saved call data for {phone_number}")


async def save_lead_data(lead_info):
    lead_info["timestamp"] = datetime.utcnow().isoformat()

    data = []
    if os.path.exists(LEAD_FILE):
        try:
            with open(LEAD_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append(lead_info)

    with open(LEAD_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[DB] Saved lead data: {lead_info.get('phone_number', 'Unknown')}")


async def get_all_leads():
    if not os.path.exists(LEAD_FILE):
        return []
    try:
        with open(LEAD_FILE, "r") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        return []
