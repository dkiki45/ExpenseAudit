# main.py
from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
import uuid 

# Importando seus módulos
from app.ocr import extract_text
from app.normalizer import normalize_receipt
from app.policy_parser import parse_policy
from app.decision_engine import evaluate_receipt
from app.audit import AuditLogger
from app.history import HistoryManager 
from app.policy_suggester import suggest_policy

app = FastAPI()
templates = Jinja2Templates(directory="templates")
history_manager = HistoryManager()

os.makedirs("samples", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    data = history_manager.get_all()
    return templates.TemplateResponse("history.html", {"request": request, "history": data})

@app.get("/tips", response_class=HTMLResponse)
def tips_page(request: Request):
    return templates.TemplateResponse("tips.html", {"request": request})

@app.post("/suggest_policy")
async def suggest_policy_endpoint(file: UploadFile):
    os.makedirs("samples", exist_ok=True)
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = f"samples/{unique_filename}"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        raw_text = extract_text(file_path)
        receipt_data = normalize_receipt(raw_text)

        
        return {"policy": suggest_policy(receipt_data)}
        
    except Exception as e:
        print(f"Suggestion Error: {e}")
        return {"policy": "Could not generate policy. Please type manually."}   

@app.post("/evaluate", response_class=HTMLResponse)
async def evaluate(
    request: Request,
    file: UploadFile,
    policy: str = Form(...) 
):
    logger = AuditLogger()
    logger.log("Initialization", "INFO", "Evaluation process initiated.")

    try:
        os.makedirs("samples", exist_ok=True)
        
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = f"samples/{unique_filename}"    
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.log("File Upload", "SUCCESS", f"File saved at: {file_path}")

    except Exception as e:
        logger.log("File Upload", "FAILURE", f"Error saving file: {str(e)}")
        return templates.TemplateResponse("result.html", {
            "request": request, 
            "error": "Upload Failed",
            "audit_log": logger.get_summary()
        })

    # OCR 
    try:
        raw_text = extract_text(file_path) 
        preview = raw_text[:50].replace('\n', ' ') + "..." if raw_text else "Empty"
        logger.log("OCR Extraction", "SUCCESS", f"Text extracted ({len(raw_text)} chars).", {"snippet": preview})
    except Exception as e:
        logger.log("OCR Extraction", "FAILURE", f"OCR Error: {str(e)}")
        return templates.TemplateResponse("result.html", {
            "request": request, 
            "error": "OCR Failed", 
            "audit_log": logger.get_summary()
        })

    # Normalizer
    receipt_data = normalize_receipt(raw_text)
    
    logger.log("Normalization", "SUCCESS", 
               f"Extracted: {receipt_data.get('currency', '$')} {receipt_data.get('amount')} | {receipt_data.get('vendor')}", 
               data=receipt_data)

    parsed_policy = parse_policy(policy)
    
    if parsed_policy.get("type") == "unknown":
        logger.log("Policy Parser", "WARNING", "Ambiguous or unknown policy.", data=parsed_policy)
    else:
        log_msg = f"Rule: {parsed_policy.get('type')} {parsed_policy.get('threshold', '')} ({parsed_policy.get('target_category', 'all')})"
        logger.log("Policy Parser", "SUCCESS", log_msg, data=parsed_policy)

    # decision_engine
    decision = evaluate_receipt(receipt_data, parsed_policy)
    
    status_decisao = "APPROVED" if decision["approved"] else "REJECTED"
    logger.log("Decision Engine", status_decisao, decision["reason"])

    history_manager.add_entry(
        filename=file.filename,
        decision=decision,
        receipt_data=receipt_data
    )

    # final
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "receipt": receipt_data,
            "decision": decision,
            "audit_log": logger.get_summary()
        }
    )