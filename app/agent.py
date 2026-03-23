from app.llm import ask_llm

def classify_intent(user_input: str) -> str:
    prompt = f"""
Determine the intent of this request.

Possible intents:
- summarize
- extract_data
- classify_clinical_workflow

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
        if (
            "billing" in text
            or "billed" in text
            or "claim" in text
            or "charged" in text
            or "balance" in text
            or "payment" in text
            or "invoice" in text
            or "coding" in text
            or "authorization" in text
            or "prior auth" in text
            or "clinical" in text
            or "chart" in text
            or "medical" in text
            or "documentation" in text
            or "portal" in text
            or "login" in text
            or "error" in text
        ):
            return "classify_clinical_workflow"
        return "summarize"

    return intent