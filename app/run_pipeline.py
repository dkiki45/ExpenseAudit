from app.ocr import extract_text
from app.normalizer import normalize_receipt
from app.policy_parser import parse_policy
from app.decision_engine import evaluate_receipt


def run(file_path: str, policy_text: str):
    raw_text = extract_text(file_path)
    receipt = normalize_receipt(raw_text)

    policy = parse_policy(policy_text)
    decision = evaluate_receipt(receipt, policy)

    return {
        "receipt": receipt,
        "policy": policy_text,
        "decision": decision
    }


if __name__ == "__main__":
    policy = "Receipts under $50 are automatically approved"
    result = run("samples/receipt.png", policy)

    print(result)
