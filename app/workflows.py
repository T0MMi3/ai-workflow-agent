import json
from pathlib import Path
from app.llm import ask_llm


KNOWLEDGE_DIR = Path("knowledge")
CLINICAL_POLICY_FILE = KNOWLEDGE_DIR / "clinical_workflow_rules.txt"


def load_clinical_workflow_rules() -> str:
    if CLINICAL_POLICY_FILE.exists():
        return CLINICAL_POLICY_FILE.read_text(encoding="utf-8")
    return "No clinical workflow rules found."


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


def classify_clinical_workflow(text: str) -> dict:
    rules = load_clinical_workflow_rules()

    prompt = f"""
You are classifying a healthcare-related workflow request using the reference below.

Workflow Rules:
{rules}

Classify this healthcare document or request into one of these categories:
- billing_review
- coding_review
- documentation_gap
- prior_authorization
- technical_issue

Return ONLY valid JSON in this exact format:
{{
  "category": "billing_review | coding_review | documentation_gap | prior_authorization | technical_issue",
  "priority": "low | medium | high",
  "recommended_action": "short_action_here"
}}

Text:
{text}
"""

    result = ask_llm(prompt)

    if result == "OPENAI_QUOTA_ERROR" or result.startswith("OPENAI_ERROR"):
        lower = text.lower()

        if any(word in lower for word in ["authorization", "prior auth", "preapproval", "approval", "referral required"]):
            return {
                "category": "prior_authorization",
                "priority": "high",
                "recommended_action": "route_to_prior_auth_queue"
            }
        elif any(word in lower for word in ["icd", "cpt", "modifier", "procedure code", "diagnosis", "coding"]):
            return {
                "category": "coding_review",
                "priority": "high",
                "recommended_action": "route_to_coding_queue"
            }
        elif any(word in lower for word in ["missing", "incomplete", "unsigned", "no signature", "missing note", "missing chart"]):
            return {
                "category": "documentation_gap",
                "priority": "medium",
                "recommended_action": "route_to_documentation_review"
            }
        elif any(word in lower for word in ["claim", "payment", "charged", "invoice", "balance", "billing", "copay", "refund"]):
            return {
                "category": "billing_review",
                "priority": "high",
                "recommended_action": "route_to_billing_queue"
            }
        elif any(word in lower for word in ["portal", "login", "timeout", "system unavailable", "upload failed", "integration issue", "error"]):
            return {
                "category": "technical_issue",
                "priority": "medium",
                "recommended_action": "route_to_technical_support"
            }
        else:
            return {
                "category": "documentation_gap",
                "priority": "low",
                "recommended_action": "route_to_manual_review"
            }

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {
            "category": "documentation_gap",
            "priority": "medium",
            "recommended_action": "manual_review_required"
        }