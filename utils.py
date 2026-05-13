import os
import json
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()


def load_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            return None, {"error": "The uploaded CSV is empty."}
        return df, None
    except Exception as e:
        return None, {"error": f"Could not read CSV: {str(e)}"}


def detect_message_column(df) -> dict:
    try:
        sample = {}
        for col in df.columns:
            sample[col] = df[col].dropna().astype(str).head(3).tolist()

        prompt = f"""
You are analysing a CSV export from a customer support system.
Here are the column names and sample values from the first few rows:

{json.dumps(sample, indent=2)}

Identify the column that contains the full customer-written message — the body text
of the support request written by a human in natural language. This is typically the
longest text field and reads like a sentence or paragraph.

A column called "message", "description", "body", "comment", or "details" is almost
certainly the right one. Prioritise columns with that name above all else.

Do NOT select: ticket_id, created_at, timestamps, email addresses, names,
short status labels, category tags, or single-word fields.

Return only this JSON, no extra text:
{{
  "column": "the column name",
  "confidence": "high or medium or low",
  "reason": "one sentence explaining your choice"
}}
"""
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        result = json.loads(raw)

        if result["column"] not in df.columns:
            return {"column": df.columns[0], "confidence": "low", "reason": "Could not detect automatically."}

        return result

    except Exception as e:
        return {"column": df.columns[0], "confidence": "low", "reason": f"Detection failed: {str(e)}"}


def extract_tickets(df, column_name: str) -> list:
    try:
        tickets = df[column_name].dropna().astype(str).tolist()
        tickets = [t.strip() for t in tickets if t.strip()]
        return tickets
    except Exception as e:
        return {"error": f"Could not extract tickets: {str(e)}"}


def group_by_category(results: list) -> dict:
    groups = {}
    for result in results:
        if "error" in result:
            continue
        category = result.get("category", "Other")
        if category not in groups:
            groups[category] = []
        groups[category].append(result)
    return groups


def get_summary_stats(results: list) -> dict:
    total = len(results)
    errors = sum(1 for r in results if "error" in r)
    high = sum(1 for r in results if r.get("priority") == "High")
    medium = sum(1 for r in results if r.get("priority") == "Medium")
    low = sum(1 for r in results if r.get("priority") == "Low")
    frustrated = sum(1 for r in results if r.get("sentiment") == "Frustrated")

    return {
        "total": total,
        "errors": errors,
        "high": high,
        "medium": medium,
        "low": low,
        "frustrated": frustrated
    }