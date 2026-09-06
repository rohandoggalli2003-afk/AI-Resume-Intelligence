import os
from dotenv import load_dotenv
from groq import Groq

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Create Groq client
client = Groq(api_key=api_key)

# Send test request
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Explain machine learning in one simple sentence."
        }
    ],
    temperature=0.2
)

# Print response
print("\nGroq Response:")
print(response.choices[0].message.content)