## Clinical Workflow Engine

A healthcare-focused workflow automation system that classifies clinical-style text into operational categories such as billing review, coding review, documentation gaps, prior authorization, and technical issues.

This project simulates real-world healthcare data processing pipelines by transforming unstructured text into structured workflow actions using FastAPI, rule-based logic, and an interactive frontend.

---

## Features

* **Healthcare Workflow Classification**

  * Categorizes input into:

    * billing_review
    * coding_review
    * documentation_gap
    * prior_authorization
    * technical_issue

* **Automated Routing**

  * Generates recommended next actions such as:

    * route_to_billing_queue
    * route_to_coding_queue
    * route_to_prior_auth_queue

* **FastAPI Backend**

  * REST API for processing and routing requests

* **Streamlit Frontend**

  * Interactive UI for testing and visualization

* **Fallback Logic**

  * Handles edge cases using keyword-based classification when LLM responses fail

---

## How It Works

1. User submits healthcare-related text
2. System determines the appropriate workflow
3. Text is classified using:

   * LLM-based reasoning
   * rule-based fallback logic
4. Output includes:

   * category
   * priority
   * recommended action

---

## Example

### Input

```
Claim denied due to missing prior authorization for MRI procedure.
```

### Output

```json
{
  "category": "prior_authorization",
  "priority": "high",
  "recommended_action": "route_to_prior_auth_queue"
}
```

---

## Tech Stack

* Python
* FastAPI
* Streamlit
* OpenAI API (for classification logic)
* Rule-based fallback system

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/clinical-workflow-engine.git
cd clinical-workflow-engine

python -m venv .venv
source .venv/Scripts/activate   # Windows

pip install -r requirements.txt
```

---

## Running the Application

### Start FastAPI backend

```bash
python -m uvicorn app.main:app --reload
```

### Start Streamlit frontend

```bash
streamlit run streamlit_app.py
```

Then open:

* API Docs: http://127.0.0.1:8000/docs
* UI: http://localhost:8501

---

## Use Cases

* Healthcare billing and coding workflow automation
* Clinical document triage and routing
* Data preprocessing for healthcare AI pipelines
* Simulation of healthcare operations systems

---

## Disclaimer

This project is a prototype for workflow automation and does **not** provide medical advice, diagnosis, or production-level medical coding. It uses synthetic and rule-based logic for demonstration purposes only.

---

## Future Improvements

* Replace rule-based logic with trained ML models
* Integrate real (de-identified or synthetic) healthcare datasets
* Add confidence scoring and analytics dashboard
* Deploy to cloud (AWS / GCP)
