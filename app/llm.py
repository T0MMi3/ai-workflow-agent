import os
from openai import OpenAI
from openai import OpenAIError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content or ""
    except RateLimitError:
        return "OPENAI_QUOTA_ERROR"
    except OpenAIError as e:
        return f"OPENAI_ERROR: {str(e)}"