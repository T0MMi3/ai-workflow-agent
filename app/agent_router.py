from app.llm import ask_llm
from app.workflows import summarize, extract_data, classify_clinical_workflow


def run_agent(user_input: str):
    prompt = f"""
You are an AI workflow router.

Your job is to choose exactly one tool for the user's request.

Available tools:
- summarize
- extract_data
- classify_clinical_workflow

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

User: Classify this healthcare request: Claim denied due to missing prior authorization.
Tool: classify_clinical_workflow

User request:
{user_input}
"""

    tool = ask_llm(prompt).strip().lower()

    if tool == "summarize":
        return "summarization_pipeline", summarize(user_input)
    elif tool == "extract_data":
        return "data_extraction_pipeline", extract_data(user_input)
    elif tool == "classify_clinical_workflow":
        return "clinical_document_routing_pipeline", classify_clinical_workflow(user_input)

    # Simple keyword fallback if the LLM returns something unexpected
    text = user_input.lower()
    if "summarize" in text or "summary" in text:
        return "summarization_pipeline", summarize(user_input)
    elif "extract" in text or "entity" in text or "data" in text:
        return "data_extraction_pipeline", extract_data(user_input)
    elif (
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
        or "chart" in text
        or "clinical" in text
        or "medical" in text
        or "documentation" in text
        or "login" in text
        or "portal" in text
        or "error" in text
    ):
        return "clinical_document_routing_pipeline", classify_clinical_workflow(user_input)

    return "fallback_pipeline", f"Could not confidently determine workflow for input: {user_input}"