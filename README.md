# Triage Desk

**AI-powered support ticket classifier built with Python, Streamlit, and the Gemini API**

🔗 [Live Demo](https://triage-desk.streamlit.app) | [Portfolio](https://ahsan-iqbal.netlify.app/#triage-desk) 

---

## What is this?

Triage Desk is a lightweight AI tool that classifies customer support tickets automatically, categorising them, assigning priority, detecting customer sentiment, and suggesting the next action. It supports both single ticket analysis and bulk CSV uploads, and groups similar tickets together to make review and analysis easier.

It was built as a portfolio project to develop practical experience with LLM API integration, prompt engineering and public deployment. I have a background in customer support and operations, so I built this with the idea that it should be something I would find helpful to use in that environment. 

---

## The problem it solves

Support teams working at scale face a consistent set of friction points that slow down resolution time and create uneven workload distribution:

- Tickets arrive unstructured and unsorted, forcing agents to manually read and triage before they can act
- There's no automatic way to identify which tickets are genuinely urgent versus routine
- Duplicate issues — multiple customers asking the same question — get handled individually rather than in bulk, wasting time
- Sentiment and urgency signals buried in ticket text go unnoticed until a customer escalates

Triage Desk aims to address all four of these without requiring any changes to existing tooling. It works with a CSV export from any support platform — Zendesk, Intercom, Freshdesk, or a simple spreadsheet.

---

## Features

**Smart classification** — each ticket is analysed by Gemini and returned with a structured classification:
- Category (Billing, Technical Issue, Account Access, Feature Request, Complaint, Other)
- Priority (High, Medium, Low) with a one-line reason
- Suggested action (Escalate to technical team, Standard response, Follow-up required, etc.)
- Customer sentiment (Frustrated, Neutral, Positive)
- A plain-English summary of the ticket

**Bulk CSV upload** — upload an export from any support tool. Triage Desk uses Gemini to automatically identify which column contains the customer message, removing the need to reformat your data before use. A confirmation step lets you verify or override the detected column before classification runs.

<img width="3838" height="1890" alt="Triage desk SS 1" src="https://github.com/user-attachments/assets/ef49040f-3c30-4b8d-a9c5-25818d1052c6" />
<img width="3834" height="1878" alt="TD SS 2" src="https://github.com/user-attachments/assets/33270288-9fa4-46ba-87fb-e00c55e671ae" />

**Duplicate grouping** — classified tickets are grouped by category in the Bulk Groups view, making it easy to identify clusters of similar issues and draft a single response that applies to all of them.
<img width="3840" height="1873" alt="TD SS 3" src="https://github.com/user-attachments/assets/a6fcf99a-b4cb-498a-b403-18f6c9ddbf28" />

**Insights** — a visual summary of your ticket batch by category, priority, and sentiment, giving support managers an immediate overview of what's coming in.
<img width="3840" height="2154" alt="TD SS 4" src="https://github.com/user-attachments/assets/5b1a6224-ad9a-4612-8a12-f49ac9e33a7a" />

**Export** — results can be downloaded as a CSV, ready to feed back into your ticketing system or share with your team.

---

## Design decisions worth noting

**Why Gemini?** The free tier is generous enough to run meaningful demos without requiring a payment, which means anyone reviewing this project can test it immediately. The tool is built to accept a user-supplied API key so there's no dependency on mine.

**Why structured JSON output?** LLMs are inconsistent by default. The prompt engineering in this project explicitly constrains output format and field values, making classifications reliable and parseable. The classifier includes defensive handling for cases where the model doesn't comply with the format instructions.

**Why a separate column detection step?** Support data comes out of different tools with different column names. Rather than requiring users to reformat their CSV, Triage Desk sends a sample of column names and values to Gemini and asks it to identify the message field automatically. This makes the tool genuinely data-source agnostic.

---

## How to run it locally

**Prerequisites:** Python 3.8+, a free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

```bash
# Clone the repo
git clone https://github.com/ahsaniqbal-projects/triage-desk.git
cd triage-desk

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
# Create a .env file with: GEMINI_API_KEY=your_key_here

# Run the app
streamlit run app.py
```

---

## Project structure

```
triage-desk/
├── app.py           # Streamlit UI — all pages and navigation
├── classifier.py    # Gemini API integration and classification logic
├── prompts.py       # Prompt templates — kept separate for easy iteration
├── utils.py         # CSV loading, column detection, grouping, stats
├── sample_data/
│   └── sample_tickets.csv   # Demo data for testing
└── .env             # Your API key (not committed to GitHub)
```

---

## What I'd build next

This version demonstrates the core concept. With more time, the next meaningful additions would be:

- **Auto-assignment**: distribute tickets evenly across agents or route them by category to the right team
- **Response drafting**: generate a suggested reply for each ticket, not just a suggested action
- **Multi-provider support**: allow users to plug in an OpenAI or Anthropic key instead of Gemini
- **Webhook integration**: connect directly to Zendesk or Intercom so tickets are classified in real time rather than via CSV export
- **Custom classification rules**: let support managers define their own priority signals in plain English, which the model applies at classification time

---

## About

Built by **Ahsan Iqbal**. I'm an operations professional with 10 years at Apple across AppleCare, Business Partner Relations, and Recruitment Operations.

This project was built as a demonstration of what I've learned so far, and I plan to keep building on it. 

→ [Portfolio](https://ahsan-iqbal.netlify.app/) 
