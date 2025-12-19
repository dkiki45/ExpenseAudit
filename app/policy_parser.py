import re

def parse_policy(policy_text: str) -> dict:
    policy_text = policy_text.lower()
    
    # try to identify the category specific in the phrase 
    category = "any"
    if "meal" in policy_text or "food" in policy_text:
        category = "Meal"
    elif "hotel" in policy_text:
        category = "Hotel"

    # Regex to capture values
    under_match = re.search(r"under\s+\$?(\d+)", policy_text)
    
    if under_match:
        return {
            "type": "under",
            "threshold": float(under_match.group(1)), 
            "target_category": category
        }

    if "always approve" in policy_text:
        return {"type": "always", "target_category": "any"}

    return {"type": "unknown", "raw_text": policy_text}