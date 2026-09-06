import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def clean_json_response(result):

    if not result:
        raise ValueError("Groq returned an empty response.")

    result = result.strip()

    if result.startswith("```json"):
        result = result[7:]

    elif result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Groq returned invalid JSON.\n\n"
            f"Response received:\n{result}\n\n"
            f"JSON error: {e}"
        )


def analyze_resume(resume_text):

    prompt = f"""
You are an expert resume analyzer.

Analyze the following resume and return ONLY a valid JSON object.

RESUME:
----------------
{resume_text}
----------------

Return exactly this JSON structure:

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "strengths": [],
    "weaknesses": []
}}

IMPORTANT RULES:

1. Return ONLY JSON.
2. Do not use markdown.
3. Do not use ```json.
4. Do not add explanations.
5. Use an empty string when information is not available.
6. Use an empty array when no items are found.
7. Make sure the JSON is valid.
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a resume analysis API. "
                    "Always return valid JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        response_format={
            "type": "json_object"
        }
    )

    result = response.choices[0].message.content

    return clean_json_response(result)