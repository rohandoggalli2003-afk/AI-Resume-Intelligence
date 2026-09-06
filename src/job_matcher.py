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


def analyze_job_match(resume_text, job_description):

    prompt = f"""
You are an expert technical recruiter.

Compare the candidate's resume with the job description.

RESUME:
----------------
{resume_text}
----------------

JOB DESCRIPTION:
----------------
{job_description}
----------------

Return ONLY a valid JSON object.

Use exactly this structure:

{{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "skill_gaps": [],
    "experience_score": 0,
    "education_score": 0,
    "experience_match": "",
    "recommendation": ""
}}

RULES:

1. match_score must be between 0 and 100.
2. experience_score must be between 0 and 100.
3. education_score must be between 0 and 100.
4. matched_skills must contain skills demonstrated in the resume
   that are relevant to the job description.
5. missing_skills must contain important job requirements that
   are not demonstrated in the resume.
6. strengths must explain why the candidate matches.
7. skill_gaps must identify areas the candidate should improve.
8. experience_score should evaluate how closely the candidate's
   projects, internships, or work experience match the role.
9. education_score should evaluate how closely the candidate's
   education matches the educational requirements.
10. experience_match should briefly explain the experience match.
11. recommendation should give a final hiring recommendation.
12. Return ONLY JSON.
13. Do not use markdown.
14. Do not use ```json.
15. Do not add explanations outside the JSON.
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a job matching API. "
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