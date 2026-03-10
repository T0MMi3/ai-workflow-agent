import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("workflow_logs.jsonl")

def log_workflow(input_text: str, intent: str, result: str, workflow: str) -> None:
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": input_text,
        "intent": intent,
        "workflow": workflow,
        "result": result
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")