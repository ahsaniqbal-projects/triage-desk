import time
import os
import json
from google import genai
from dotenv import load_dotenv
from prompts import CLASSIFIER_PROMPT

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def classify_ticket(ticket_text: str) -> dict:
    if not ticket_text or not ticket_text.strip():
        return {"error": "No ticket text provided."}

    try:
        full_prompt = f"{CLASSIFIER_PROMPT}\n\nTicket:\n{ticket_text.strip()}"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        time.sleep(6)
        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError:
        return {"error": "Gemini returned an unexpected format. Please try again."}
    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}