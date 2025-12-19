import math

def suggest_policy(receipt_data: dict) -> str:
    category = receipt_data.get("category", "General")
    amount = receipt_data.get("amount")
    
    if amount is None:
        amount = 0
    
    suggested_limit = math.ceil(amount / 10) * 10
    if suggested_limit == 0: suggested_limit = 50

    return (
        f'If the expense category is "{category}" '
        f'and the amount is under {suggested_limit}, approve.'
    )