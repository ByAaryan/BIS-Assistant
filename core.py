from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()


# =========================================================
# Notes
# =========================================================

def load_data():
    try:
        with open("notes.json", "r") as file:
            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data):
    with open("notes.json", "w") as file:
        json.dump(data, file, indent=2)


def save_response(response, question):
    data = load_data()

    data.append({
        "question": question,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "response": response
    })

    save_data(data)


# =========================================================
# BIS Assistant
# =========================================================

def analyze_product(
    business,
    product,
    description,
    intended_use,
    target_market,
    existing_certification
):

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""
You are a BIS (Bureau of Indian Standards) AI assistant.

Analyze the following business and product.

BUSINESS / INDUSTRY:
{business}

PRODUCT:
{product}

PRODUCT DESCRIPTION:
{description}

INTENDED USE:
{intended_use}

TARGET MARKET:
{target_market}

EXISTING CERTIFICATION:
{existing_certification}

Your task is to provide useful guidance regarding Indian Standards,
BIS certification, testing and the certification process.

IMPORTANT RULES:

1. Do NOT invent Indian Standard numbers.
2. Do NOT invent certification schemes.
3. Do NOT invent legal requirements.
4. If information is uncertain, explicitly say that it needs
   verification from official BIS sources.
5. Distinguish between mandatory requirements and general guidance.
6. Give practical information suitable for a business owner.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "summary": "Short summary of the product's BIS requirements",

    "standards": [
        {{
            "name": "IS XXXXX",
            "title": "Standard title",
            "relevance": "Why this standard may apply",
            "mandatory": "Yes / No / Needs verification"
        }}
    ],

    "certification": {{
        "required": "Yes / No / Needs verification",
        "scheme": "Relevant BIS certification scheme if known",
        "details": "Explanation"
    }},

    "testing": [
        "Testing requirement 1",
        "Testing requirement 2"
    ],

    "process": [
        "Step 1",
        "Step 2",
        "Step 3",
        "Step 4"
    ],

    "documents": [
        "Document 1",
        "Document 2",
        "Document 3"
    ],

    "additional_requirements": [
        "Additional requirement 1",
        "Additional requirement 2"
    ],

    "warnings": [
        "Important thing the business should verify"
    ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    raw_response = response.text.strip()

    # Remove markdown JSON fences if Gemini adds them
    if raw_response.startswith("```"):
        raw_response = raw_response.replace("```json", "")
        raw_response = raw_response.replace("```", "")
        raw_response = raw_response.strip()

    try:
        result = json.loads(raw_response)

    except json.JSONDecodeError:
        # Save the raw response for debugging
        save_response(
            raw_response,
            f"{business} - {product}"
        )

        raise ValueError(
            "Gemini returned an invalid JSON response."
        )

    # Save structured response
    save_response(
        json.dumps(result, indent=2),
        f"{business} - {product}"
    )

    return result