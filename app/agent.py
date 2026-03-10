from app.llm import ask_llm

def classify_intent(user_input: str) -> str:
    prompt = f"""
Determine the intent of this request.

Possible intents:
- summarize
- extract_data
- classify_ticket

Request:
{user_input}

Return ONLY the intent name.
"""

    intent = ask_llm(prompt).strip().lower()

    if intent == "openai_quota_error" or intent.startswith("openai_error"):
        text = user_input.lower()
        if "summarize" in text:
            return "summarize"
        if "extract" in text or "data" in text:
            return "extract_data"
        if "ticket" in text or "billing" in text or "support" in text:
            return "classify_ticket"
        return "summarize"

    return intent