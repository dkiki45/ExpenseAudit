def evaluate_receipt(receipt, policy):
    # 1. Sanity Check
    if policy.get("type") == "unknown":
        return {"approved": False, "reason": "Policy could not be understood."}
        
    if not receipt["receipt_provided"] or receipt["amount"] is None:
        return {"approved": False, "reason": "Could not read receipt data."}

    # 2. Category Compatibility Check (Advanced Business Rule)
    # If policy is specific (e.g., Meal) and receipt is another (e.g., Hotel)
    if policy.get("target_category") != "any" and policy.get("target_category") != receipt["category"]:
        return {
            "approved": False, 
            "reason": f"Policy applies to {policy['target_category']}, but receipt is {receipt['category']}."
        }

    # 3. Value Logic
    if policy["type"] == "under":
        limit = policy["threshold"] 
        amount = receipt["amount"]
        
        if amount <= limit:
            return {
                "approved": True,
                "reason": f"Amount {amount} is within the limit of {limit}."
            }
        else:
            return {
                "approved": False,
                "reason": f"Amount {amount} exceeds the limit of {limit}."
            }

    if policy["type"] == "always":
        return {"approved": True, "reason": "Automatic approval policy."}

    return {"approved": False, "reason": "Rule not applicable."}