# ExpenseAudit
ExpenseAudit is a Travel &amp; Expense decision automation platform that evaluates receipts using policies written in structured natural language (English-as-Code).

## English-as-Code

Instead of hard-coding business rules or relying on opaque models, policies are written in plain, structured English that can be read, validated, and reasoned about by both technical and non-technical stakeholders.

## Architecture
The platform is designed around a deterministic and explainable decision pipeline.
Each step transforms unstructured input into auditable business logic outcomes.

Receipt Upload -> OCR / Text Extraction -> Data Normalization (amount, date, category, vendor) -> English-as-Code Policy Engine -> Deterministic Decision Engine -> Decision Output (Approve / Reject + Explanation) -> Audit Trail & Expense History

## Local Setup
To run the project locally: 

- git clone https://github.com/dkiki45/ExpenseAudit.git
- cd ExpenseAudit

- python -m venv .venv
- source .venv/bin/activate

- pip install -r requirements.txt

- uvicorn app.main:app --reload

Once the server is running, access the platform at:
- http://127.0.0.1:8000


