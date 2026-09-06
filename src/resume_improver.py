import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def improve_resume(resume_text, job_description):

    prompt = f"""
You are an expert resume improvement assistant.

Analyze the resume against the job description.

RESUME:
----------------
{resume_text}
----------------

JOB DESCRIPTION:
----------------
{job_description}
----------------

Provide useful resume improvement suggestions.

IMPORTANT:
- Do not invent skills.
- Do not invent experience.
- Do not invent projects.
- Do not invent certifications.
- Do not invent achievements.
- Do not invent numbers.
- Only use information supported by the resume.
- Keep suggestions concise.
- Maximum 3 priority actions.
- Maximum 5 keyword suggestions.
- Maximum 3 project improvements.
- Maximum 2 bullet rewrites.

Return the information using the exact required fields.
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert resume improvement assistant. "
                    "Return only the requested structured JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1,

        reasoning_effort="low",

        max_completion_tokens=3000,

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_improvement",
                "strict": True,

                "schema": {
                    "type": "object",

                    "properties": {

                        "overall_advice": {
                            "type": "string"
                        },

                        "priority_actions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },

                        "keyword_suggestions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },

                        "project_improvements": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },

                        "bullet_rewrites": {
                            "type": "array",
                            "items": {

                                "type": "object",

                                "properties": {

                                    "original": {
                                        "type": "string"
                                    },

                                    "improved": {
                                        "type": "string"
                                    },

                                    "reason": {
                                        "type": "string"
                                    }

                                },

                                "required": [
                                    "original",
                                    "improved",
                                    "reason"
                                ],

                                "additionalProperties": False
                            }
                        }
                    },

                    "required": [
                        "overall_advice",
                        "priority_actions",
                        "keyword_suggestions",
                        "project_improvements",
                        "bullet_rewrites"
                    ],

                    "additionalProperties": False
                }
            }
        }
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError(
            "Groq returned an empty response."
        )

    return json.loads(result)