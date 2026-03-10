from fastapi import FastAPI
from pydantic import BaseModel

from app.agent_router import run_agent
from app.logger import log_workflow

app = FastAPI()


class Request(BaseModel):
    text: str


@app.post("/process")
def process_request(req: Request):
    workflow_name, result = run_agent(req.text)

    log_workflow(
        input_text=req.text,
        intent="agent_selected",
        result=str(result),
        workflow=workflow_name
    )

    return {
        "intent": "agent_selected",
        "workflow": workflow_name,
        "result": result
    }