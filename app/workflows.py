import json
from pathlib import Path
from app.llm import ask_llm


KNOWLEDGE_DIR = Path("knowledge")
TICKET_POLICY_FILE = KNOWLEDGE_DIR / "ticket_policies.txt"


def load_ticket_policies() -> str:
    if TICKET_POLICY_FILE.exists():
        return TICKET_POLICY_FILE.read_text(encoding="utf-8")
    return "No ticket policies found."


def summarize(text: str) -> str:
    prompt = f"Summarize the following text:\n{text}"
    result = ask_llm(prompt)

    if result == "OPENAI_QUOTA_ERROR" or result.startswith("OPENAI_ERROR"):
        return f"Fallback summary: {text[:120]}..."

    return result


def extract_data(text: str) -> str:
    prompt = f"""
Extract important entities from this text.
Return as valid JSON.

Text:
{text}
"""
    result = ask_llm(prompt)

    if result == "OPENAI_QUOTA_ERROR" or result.startswith("OPENAI_ERROR"):
        return json.dumps({
            "entities": ["fallback_mode"],
            "note": "OpenAI unavailable"
        })

    return result


def classify_ticket(text: str) -> dict:
    policies = load_ticket_policies()

    prompt = f"""
You are classifying a support ticket using the policy reference below.

Policy Reference:
{policies}

Classify this support ticket.

Categories:
- billing
- technical
- general

Return ONLY valid JSON in this exact format:
{{
  "category": "billing | technical | general",
  "priority": "low | medium | high",
  "recommended_action": "short_action_here"
}}

Ticket:
{text}
"""

    result = ask_llm(prompt)

    if result == "OPENAI_QUOTA_ERROR" or result.startswith("OPENAI_ERROR"):
        lower = text.lower()

        if "bill" in lower or "payment" in lower or "charged" in lower:
            return {
                "category": "billing",
                "priority": "high",
                "recommended_action": "route_to_finance_queue"
            }
        elif "error" in lower or "bug" in lower or "login" in lower:
            return {
                "category": "technical",
                "priority": "medium",
                "recommended_action": "route_to_technical_support"
            }
        else:
            return {
                "category": "general",
                "priority": "low",
                "recommended_action": "route_to_general_support"
            }

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {
            "category": "general",
            "priority": "medium",
            "recommended_action": "manual_review_required"
        }