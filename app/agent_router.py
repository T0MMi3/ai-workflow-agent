from app.llm import ask_llm
from app.workflows import summarize, extract_data, classify_ticket


def run_agent(user_input: str):
    prompt = f"""
You are an AI workflow router.

Your job is to choose exactly one tool for the user's request.

Available tools:
- summarize
- extract_data
- classify_ticket

Rules:
- Return ONLY one exact tool name
- Do not explain
- Do not add punctuation
- Do not add extra words

Examples:
User: Summarize this article about healthcare automation.
Tool: summarize

User: Extract data from this text: John Smith visited Dallas on March 1.
Tool: extract_data

User: Classify this support ticket: I was charged twice.
Tool: classify_ticket

User request:
{user_input}
"""

    tool = ask_llm(prompt).strip().lower()

    if tool == "summarize":
        return "summarization_pipeline", summarize(user_input)
    elif tool == "extract_data":
        return "data_extraction_pipeline", extract_data(user_input)
    elif tool == "classify_ticket":
        return "ticket_classification_pipeline", classify_ticket(user_input)

    # Simple keyword fallback if the LLM returns something unexpected
    text = user_input.lower()
    if "summarize" in text or "summary" in text:
        return "summarization_pipeline", summarize(user_input)
    elif "extract" in text or "entity" in text or "data" in text:
        return "data_extraction_pipeline", extract_data(user_input)
    elif "ticket" in text or "billing" in text or "charged" in text or "login" in text or "error" in text:
        return "ticket_classification_pipeline", classify_ticket(user_input)

    return "fallback_pipeline", f"Could not confidently determine workflow for input: {user_input}"